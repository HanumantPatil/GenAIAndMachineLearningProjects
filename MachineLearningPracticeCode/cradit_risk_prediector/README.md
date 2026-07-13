---
title: Credit Risk Predictor
description: Credit risk modeling notebooks and datasets for default prediction, feature engineering, and rank-order evaluation.
author: GitHub Copilot
ms.date: 2026-07-06
ms.topic: overview
keywords:
  - credit risk
  - default prediction
  - feature engineering
  - optuna
  - ks statistic
estimated_reading_time: 5
---

## Overview

This folder contains the end-to-end credit risk workflow for a borrower default-risk scoring prototype. The notebooks in this directory show how the training data is assembled, how features are engineered, how the model is tuned, and how the final scorecard-style output is produced for the Streamlit app.

The application path is:

1. Gather borrower and loan inputs from the UI.
2. Convert the raw inputs into the trained model's feature schema.
3. Scale the fields that were scaled during training.
4. Run the saved model bundle from `artifacts/model_data.joblib`.
5. Return probability of default, a credit score, and a qualitative rating.

## Contents

* `main.py`: Streamlit interface for entering applicant data and displaying the score.
* `prediection_helper.py`: Prediction helper that loads the trained bundle, prepares features, and computes the score.
* `cradit_risk_model.ipynb`: Main notebook covering data merge, cleaning, feature engineering, feature selection, and model training.
* `optuna_example.ipynb`: Hyperparameter tuning experiments for candidate models.
* `customers.csv`: Customer demographic and profile data.
* `loans.csv`: Loan application and repayment data.
* `bureau_data.csv`: Bureau and credit history features.
* `RankOrder_KSStatistic/`: Supporting material for rank-order and KS evaluation.
* `artifacts/model_data.joblib`: Saved training bundle containing the fitted model, scaler, feature list, and scaling columns.
* `BAK/`: Backup or intermediate artifacts used as fallback locations when loading the bundle.
* `SOW Credit Risk Model.pdf`: Project scope document.

## Workflow

1. Load and merge customer, loan, and bureau data.
2. Clean missing values and normalize categorical values.
3. Engineer features such as loan-to-income, delinquency ratio, average DPD per delinquency, and one-hot encoded categorical indicators.
4. Reduce multicollinearity and evaluate predictive power with VIF and IV.
5. Train and compare classification models.
6. Package the selected model, scaler, and feature metadata into `model_data.joblib`.
7. Serve the trained bundle through the helper module and Streamlit app.
8. Evaluate ranking performance with ROC, deciles, and KS-style tables.

## Prediction Inputs

The Streamlit app currently accepts the following values:

* `age`
* `income`
* `loan_amount`
* `loan_tenure_months`
* `avg_dpd_per_delinquency`
* `delinquency_ratio`
* `credit_utilization_ratio`
* `num_open_accounts`
* `residence_type`
* `loan_purpose`
* `loan_type`

The helper derives `loan_to_income` from `loan_amount / income` and converts the categorical fields into indicator columns.

## Output

The app returns three values:

* Probability of default as a percentage.
* Credit score on a 300 to 900 style scale.
* Human-readable rating: Poor, Average, Good, Excellent, or Undefined.

The score buckets are implemented in `prediection_helper.py` and are intended for quick interpretation rather than regulatory-grade scorecarding.

## How to Run

```powershell
# Activate the workspace environment
.\.venv\Scripts\Activate.ps1

# Launch the Streamlit app from this folder
python -m streamlit run cradit_risk_prediector\main.py
```

### Streamlit UI

Use the Python module form when launching the app with `uv` on Windows. This avoids the `uv trampoline failed to canonicalize script path` launcher issue.

```powershell
uv run --with streamlit python -m streamlit run cradit_risk_prediector/main.py
```

If you are already inside `cradit_risk_prediector/`, the shorter form also works:

```powershell
uv run --with streamlit python -m streamlit run main.py
```

### Notebook Workflow

If you want to explore or retrain the model, open `cradit_risk_model.ipynb` from this folder so the CSV files resolve correctly.

## Notes

* The folder name keeps the original project spelling.
* The helper loads the model bundle from the first matching artifact path, so older backup folders continue to work.
* The `prediection_helper.py` file name is preserved for compatibility with the existing imports.
