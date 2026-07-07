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

This folder contains the end-to-end credit risk workflow. It combines customer, loan, and bureau data to model default risk, then explores feature engineering, multicollinearity checks, and rank-order and KS-style evaluation.

## Contents

* `cradit_risk_model.ipynb`: Main notebook covering data merge, cleaning, feature engineering, feature selection, and model training.
* `optuna_example.ipynb`: Hyperparameter tuning experiments for candidate models.
* `customers.csv`: Customer demographic and profile data.
* `loans.csv`: Loan application and repayment data.
* `bureau_data.csv`: Bureau and credit history features.
* `RankOrder_KSStatistic/`: Supporting material for rank-order and KS evaluation.
* `BAK/`: Backup or intermediate artifacts.
* `SOW Credit Risk Model.pdf`: Project scope document.

## Workflow

1. Load and merge customer, loan, and bureau data.
2. Clean missing values and inconsistent categorical values.
3. Engineer features such as loan-to-income, delinquency ratio, and average DPD per delinquency.
4. Reduce multicollinearity and evaluate predictive power with VIF and IV.
5. Train and compare classification models.
6. Evaluate ranking performance with ROC, deciles, and KS-style tables.

## How to Run

```powershell
# Activate the workspace environment
.\.venv\Scripts\Activate.ps1

# Open the notebook from this folder
jupyter notebook cradit_risk_model.ipynb
```

## Notes

* The folder name keeps the original project spelling.
* Run the notebook from this directory so the local CSV files resolve correctly.
