from fastapi import FastAPI
from prediection_helper import predict
from pydantic import BaseModel

# Create the FastAPI application instance used by Uvicorn.
app = FastAPI()
# .\Cradit_Risk_api\main.ps1


class CreditRiskInput(BaseModel):
    age: int
    income: float
    loan_amount: float
    loan_tenure_months: int
    avg_dpd_per_delinquency: float
    delinquency_ratio: float
    credit_utilization_ratio: float
    num_open_accounts: int
    residence_type: str
    loan_purpose: str
    loan_type: str


class CreditRiskOutput(BaseModel):
    probability: float
    credit_score: int
    rating: str


@app.get("/ping")
def ping():
    # Lightweight health endpoint to confirm the API is alive.
    return {"ping": "pong"}

@app.post("/predict", response_model=CreditRiskOutput)
def predict_credit_risk(input_data: CreditRiskInput):
    """Run the full credit-risk scoring pipeline for a single applicant."""
    try:
        probability, credit_score, rating = predict(
            input_data.age,
            input_data.income,
            input_data.loan_amount,
            input_data.loan_tenure_months,
            input_data.avg_dpd_per_delinquency,
            input_data.delinquency_ratio,
            input_data.credit_utilization_ratio,
            input_data.num_open_accounts,
            input_data.residence_type,
            input_data.loan_purpose,
            input_data.loan_type,
        )
        return CreditRiskOutput(
            probability=probability, credit_score=credit_score, rating=rating
        )
    except Exception as e:
        # Handle any unexpected errors gracefully and return a 500 response.
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn

    # Run directly with: python .\Cradit_Risk_api\main.py
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
