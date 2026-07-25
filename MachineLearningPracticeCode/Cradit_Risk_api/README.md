---
title: Cradit Risk API
description: FastAPI service for credit risk scoring with health and prediction endpoints backed by the trained model bundle.
author: Hanumant Patil
ms.date: 2026-07-25
ms.topic: how-to
keywords:
  - fastapi
  - credit risk
  - machine learning
  - api
estimated_reading_time: 5
---

## Overview

Cradit Risk API is a lightweight FastAPI service that serves credit-risk predictions from the trained model artifacts. The API includes a health endpoint and a prediction endpoint that returns default probability, credit score, and risk rating.

## Folder Contents

* `main.py`: FastAPI application with `/ping` and `/predict` routes
* `prediection_helper.py`: Feature preparation and scoring logic
* `request.http`: Ready-to-run REST Client requests for local testing
* `artifacts/`: Primary model bundle location
* `BAK/`: Backup copies of historical artifacts

## Prerequisites

* Python 3.10 or later
* Virtual environment created at the repository root
* Dependencies installed from the root `requirements.txt`

## Run the API

From the repository root:

```powershell
.\.venv\Scripts\Activate.ps1
python .\Cradit_Risk_api\main.py
```

The server starts at <http://127.0.0.1:8000>.

## Endpoints

### GET /ping

Use this endpoint to verify service health.

Example request:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/ping | ConvertTo-Json -Compress
```

Expected response:

```json
{"ping":"pong"}
```

### POST /predict

Use this endpoint to get credit-risk outputs for one applicant.

Request body schema:

```json
{
  "age": 30,
  "income": 50000,
  "loan_amount": 20000,
  "loan_tenure_months": 36,
  "avg_dpd_per_delinquency": 5.0,
  "delinquency_ratio": 0.1,
  "credit_utilization_ratio": 0.3,
  "num_open_accounts": 5,
  "residence_type": "Rented",
  "loan_purpose": "Personal",
  "loan_type": "Unsecured"
}
```

Example request:

```powershell
$body = @{
  age = 30
  income = 50000
  loan_amount = 20000
  loan_tenure_months = 36
  avg_dpd_per_delinquency = 5.0
  delinquency_ratio = 0.1
  credit_utilization_ratio = 0.3
  num_open_accounts = 5
  residence_type = 'Rented'
  loan_purpose = 'Personal'
  loan_type = 'Unsecured'
} | ConvertTo-Json

Invoke-RestMethod -Uri 'http://127.0.0.1:8000/predict' -Method Post -Body $body -ContentType 'application/json'
```

Example response:

```json
{
  "probability": 0.0000018462,
  "credit_score": 899,
  "rating": "Excellent"
}
```

## Valid Categorical Values

Use these values for best alignment with model features:

* `residence_type`: `Owned` or `Rented`
* `loan_purpose`: `Education`, `Home`, or `Personal`
* `loan_type`: `Unsecured`

## Test with request.http

If you use the VS Code REST Client extension:

1. Open `Cradit_Risk_api/request.http`
2. Run the `POST /predict` request
3. Run the `GET /ping` request

The file uses `###` separators so each request can be sent independently.
