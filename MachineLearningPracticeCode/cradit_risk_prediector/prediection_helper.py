import pandas as pd
import numpy as np
from joblib import load
from pathlib import Path

# Resolve the project folder first so the helper can work whether it is executed
# from the Streamlit app, a notebook, or a direct Python import.
BASE_DIR = Path(__file__).resolve().parent

# The trained model bundle has moved around during development, so we check the
# current artifact folder first and then fall back to older backup locations.
MODEL_PATH_CANDIDATES = [
    BASE_DIR / "artifacts" / "model_data.joblib",
    BASE_DIR / "BAK" / "artifacts" / "model_data.joblib",
    BASE_DIR / "BAK" / "app" / "artifacts" / "model_data.joblib",
]

for model_path in MODEL_PATH_CANDIDATES:
    if model_path.exists():
        MODEL_PATH = model_path
        break
else:
    raise FileNotFoundError(
        "Could not find model_data.joblib in artifacts/ or BAK/ artifact folders."
    )

# Load the serialized training bundle once at import time so the app can reuse
# the trained estimator, scaler, and feature metadata for every prediction.
model_data = load(MODEL_PATH)
model = model_data["model"]
scaler = model_data["scaler"]
features = model_data["features"]
cols_to_scale = model_data["cols_to_scale"]


def prepare_input(
    age,
    income,
    loan_amount,
    loan_tenure_months,
    avg_dpd_per_delinquency,
    delinquency_ratio,
    credit_utilization_ratio,
    num_open_accounts,
    residence_type,
    loan_purpose,
    loan_type,
):
    """Create a model-ready feature frame from raw user inputs.

    The Streamlit UI only asks for the main borrower and loan attributes. The
    trained model, however, expects a wider feature set. This function bridges
    that gap by:

    1. Deriving engineered values such as loan-to-income.
    2. Encoding categorical selections as one-hot style indicator columns.
    3. Filling non-UI features with neutral placeholder values so the scaler and
       model receive the exact columns used during training.
    """

    # Create the raw input row using the user-provided values plus the derived
    # features that the model was trained on.
    input_data = {
        "age": age,
        "loan_tenure_months": loan_tenure_months,
        "number_of_open_accounts": num_open_accounts,
        "credit_utilization_ratio": credit_utilization_ratio,
        "loan_to_income": loan_amount / income if income > 0 else 0,
        "delinquency_ratio": delinquency_ratio,
        "avg_dpd_per_delinquency": avg_dpd_per_delinquency,
        "residence_type_Owned": 1 if residence_type == "Owned" else 0,
        "residence_type_Rented": 1 if residence_type == "Rented" else 0,
        "loan_purpose_Education": 1 if loan_purpose == "Education" else 0,
        "loan_purpose_Home": 1 if loan_purpose == "Home" else 0,
        "loan_purpose_Personal": 1 if loan_purpose == "Personal" else 0,
        "loan_type_Unsecured": 1 if loan_type == "Unsecured" else 0,
        # These features are required by the trained pipeline but are not
        # currently collected in the UI, so the helper supplies placeholder
        # values to keep the input schema aligned with training.
        "number_of_dependants": 1,  # Dummy value
        "years_at_current_address": 1,  # Dummy value
        "zipcode": 1,  # Dummy value
        "sanction_amount": 1,  # Dummy value
        "processing_fee": 1,  # Dummy value
        "gst": 1,  # Dummy value
        "net_disbursement": 1,  # Computed dummy value
        "principal_outstanding": 1,  # Dummy value
        "bank_balance_at_application": 1,  # Dummy value
        "number_of_closed_accounts": 1,  # Dummy value
        "enquiry_count": 1,  # Dummy value
    }

    # Build a one-row DataFrame so the scaler and feature selection logic can
    # operate on the same structure that was used during model training.
    df = pd.DataFrame([input_data])

    # Scale only the columns that were scaled during training; the feature list
    # is preserved in the bundle so the helper can stay consistent with the
    # saved model.
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    # Reorder and trim the frame to the exact model input columns.
    df = df[features]
    return df


def calculate_credit_score(input_df, base_score=300, scaling_factor=600):
    """Convert model output into probability, score, and qualitative rating.

    The estimator exposes coefficients and intercepts, so we compute the linear
    score directly, apply the logistic transform to get the default probability,
    and then map the non-default probability to a credit-score-like scale.
    """

    # Compute the linear model output manually so the helper can derive both the
    # probability of default and a readable score from the same prediction step.
    x = np.dot(input_df.values, model.coef_.T) + model.intercept_
    default_probability = 1 / (1 + np.exp(-x))
    non_default_probability = 1 - default_probability

    # Translate the non-default probability to a familiar score range.
    credit_score = base_score + scaling_factor * non_default_probability.flatten()

    def get_rating(score):
        # Keep the buckets intentionally broad so users can interpret the score
        # at a glance without needing the raw probability.
        if 300 <= score < 500:
            return "Poor"
        elif 500 <= score < 650:
            return "Average"
        elif 650 <= score < 750:
            return "Good"
        elif 750 <= score < 900:
            return "Excellent"
        else:
            return "Undefined"  # Handle scores outside the expected range

    ratings = get_rating(credit_score[0])
    return (
        default_probability.flatten()[0],
        int(credit_score),
        ratings,
    )


def predict(
    age,
    income,
    loan_amount,
    loan_tenure_months,
    avg_dpd_per_delinquency,
    delinquency_ratio,
    credit_utilization_ratio,
    num_open_accounts,
    residence_type,
    loan_purpose,
    loan_type,
):
    """Run the full credit-risk scoring pipeline for a single applicant."""

    # Convert the raw form values into the exact feature matrix expected by the
    # trained model.
    df = prepare_input(
        age,
        income,
        loan_amount,
        loan_tenure_months,
        avg_dpd_per_delinquency,
        delinquency_ratio,
        credit_utilization_ratio,
        num_open_accounts,
        residence_type,
        loan_purpose,
        loan_type,
    )

    # Derive the final model outputs in the same order the UI expects.
    probability, credit_score, rating = calculate_credit_score(df)

    return probability, credit_score, rating
