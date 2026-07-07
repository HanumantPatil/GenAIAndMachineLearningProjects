# Logistic Regression

## Overview

This folder contains implementations of **Logistic Regression**, a fundamental classification algorithm that models the probability of binary outcomes using the logistic function.

## Key Concepts

- **Logistic Regression**: Binary/multi-class classification
- **Logistic Function**: Sigmoid curve mapping outputs to [0,1]
- **Log-Odds**: Logarithm of odds ratio
- **Maximum Likelihood Estimation**: Optimal parameter fitting
- **Probability Calibration**: Confidence in predictions
- **Decision Boundary**: Classification threshold

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
scipy
```

## Key Learning Outcomes

✓ Logistic regression for binary classification
✓ Probability interpretation
✓ Log-odds and odds ratios
✓ Coefficient interpretation
✓ Decision boundary visualization
✓ Multi-class logistic regression (One-vs-Rest)
✓ Regularization in logistic regression (L1, L2)
✓ Threshold optimization for imbalanced data
✓ Model evaluation metrics (Accuracy, Precision, Recall, F1, AUC-ROC)
✓ Feature scaling importance

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run notebooks or scripts in this folder
jupyter notebook *.ipynb
python *.py
```

## Logistic Regression Variants

✓ **Binary Logistic Regression**: Two classes (0/1)
✓ **Multi-class Logistic Regression**: Three+ classes
✓ **Multinomial Logistic Regression**: Softmax for multiple classes
✓ **Ordinal Logistic Regression**: Ordered categories

## Model Equations

**Logistic Function (Sigmoid)**
```
P(y=1|x) = 1 / (1 + e^(-z))
where z = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ
```

**Log-Odds**
```
log(odds) = log(P(y=1)/P(y=0)) = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ
```

## Best Practices

- Standardize/normalize features
- Check for multicollinearity
- Use regularization to prevent overfitting
- Choose appropriate threshold (not always 0.5)
- Evaluate with appropriate metrics for problem type
- Interpret coefficients in terms of log-odds
- Validate on held-out test set
- Use cross-validation for robust evaluation

## Evaluation Metrics

✓ **Accuracy**: Overall correctness
✓ **Precision**: Positive predictive value
✓ **Recall (Sensitivity)**: True positive rate
✓ **Specificity**: True negative rate
✓ **F1-Score**: Harmonic mean of precision and recall
✓ **AUC-ROC**: Area under receiver operating characteristic curve
✓ **Confusion Matrix**: Detailed prediction breakdown

## Key Learnings

✓ Logistic regression is interpretable linear classifier
✓ Probabilities directly interpretable
✓ Foundation for many advanced algorithms
✓ Efficient and scalable
✓ Works well with feature engineering
✓ Suitable for business applications requiring interpretability
