---
title: PracticeCode
description: Python and machine learning practice repository with scripts, notebooks, and sample datasets for statistics and regression exercises.
---

## Overview

PracticeCode is a hands-on learning repository for Python, NumPy, pandas, statistics, and machine learning fundamentals. It includes standalone scripts, Jupyter notebooks, and CSV datasets used across topics like distributions, confidence intervals, regression, encoding, and model evaluation.

## Repository Structure

* `num.py`, `number.py`, `numpy_examples.py`, `pandas01.py`: Core Python and data library practice scripts
* `bill_survey.csv`, `heights.csv`, `miles.csv`, `shoe_sales.csv`: Root-level datasets
* `GradientDescent/`: Gradient descent implementations and home price dataset
* `House_Prediector_Model/`: Linear regression notebooks and housing datasets
* `LLD/`: Basic low-level design class practice
* `ModelEvalution/`: Train/test split tutorials and evaluation notebooks
* `OneHotEncoding/`: One-hot encoding notebooks and dataset
* `PolynomialRegression/`: Polynomial regression notebooks and car price dataset
* Root notebooks: Statistics and probability practice such as central limit theorem, confidence scores, confidence intervals, and height analysis

## Updated Solutions

* Added an updated income bucket analysis in `health_insurance_cost_prediector/data_cleaning/ml_premium_prediction_imp.ipynb` using `pd.cut` and `pd.crosstab`.
* The income ranges are grouped as `<10L`, `10L-25L`, `25L-40L`, and `>40L` before generating the contingency table.
* The notebook now visualizes this grouped crosstab with a stacked bar chart and uses the same `crosstab` output for the heatmap.

## Prerequisites

* Python 3.10 or later
* `pip`

## Environment Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## How to Run

Run a Python script:

```powershell
python number.py
python numpy_examples.py
python pandas01.py
```

Open notebooks from the workspace in VS Code and run cells using the selected Python kernel from `.venv`.

## Notes

* Folder names are kept as-is to preserve existing notebook paths and references.
* Some topic folders contain similarly named datasets for isolated practice scenarios.
