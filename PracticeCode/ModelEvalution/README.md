# Model Evaluation

## Overview

This folder contains comprehensive resources on **model evaluation techniques** essential for assessing machine learning model performance, ensuring generalization, and making informed model selection decisions.

## Key Concepts

- **Evaluation Metrics**: Quantifying model performance
- **Validation Strategies**: Robust performance estimation
- **Overfitting Detection**: Identifying model capacity issues
- **Cross-Validation**: Multiple fold evaluation
- **Performance Trade-offs**: Accuracy vs Interpretability
- **Baseline Comparison**: Benchmarking against simple models

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
```

## Key Learning Outcomes

✓ Classification metrics (Accuracy, Precision, Recall, F1)
✓ Regression metrics (MSE, RMSE, MAE, R²)
✓ ROC curves and AUC score
✓ Confusion matrix interpretation
✓ Cross-validation strategies
✓ Overfitting and underfitting detection
✓ Learning curves for diagnosis
✓ Hyperparameter tuning effects
✓ Multiple model comparison
✓ Performance trade-offs

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run notebooks or scripts in this folder
jupyter notebook *.ipynb
python *.py
```

## Classification Metrics

### Accuracy
```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
Best for: Balanced classification
```

### Precision
```
Precision = TP / (TP + FP)
Measures: % of positive predictions that are correct
Best for: Minimizing false positives
```

### Recall (Sensitivity)
```
Recall = TP / (TP + FN)
Measures: % of actual positives identified
Best for: Minimizing false negatives
```

### F1-Score
```
F1 = 2 * (Precision * Recall) / (Precision + Recall)
Best for: Imbalanced data, balanced metric
```

### Specificity
```
Specificity = TN / (TN + FP)
Measures: % of actual negatives identified
```

### AUC-ROC
```
AUC = Area Under ROC Curve
Range: [0, 1]
> 0.5: Better than random
= 0.5: Random guessing
= 1.0: Perfect classifier
```

## Regression Metrics

### Mean Absolute Error (MAE)
```
MAE = Σ|y - ŷ| / n
Interpretation: Average absolute error in same units as target
```

### Mean Squared Error (MSE)
```
MSE = Σ(y - ŷ)² / n
Interpretation: Average squared error, penalizes large errors
```

### Root Mean Squared Error (RMSE)
```
RMSE = √MSE
Interpretation: Square root of MSE, same units as target
```

### R² Score (Coefficient of Determination)
```
R² = 1 - (SS_res / SS_tot)
Range: [0, 1] (can be negative for bad models)
Interpretation: Proportion of variance explained
```

## Confusion Matrix

```
                Predicted
            Positive | Negative
Actual  P | TP      | FN
        N | FP      | TN

TP: True Positive - correctly predicted positive
TN: True Negative - correctly predicted negative
FP: False Positive - incorrectly predicted positive (Type I error)
FN: False Negative - incorrectly predicted negative (Type II error)
```

## ROC Curve

- **X-axis**: False Positive Rate (FPR)
- **Y-axis**: True Positive Rate (TPR)
- **Diagonal**: Random classifier performance
- **Above Diagonal**: Better than random
- **AUC**: Area under the curve (0 to 1)

## Cross-Validation

### K-Fold Cross-Validation
```
1. Divide data into k folds
2. For each fold:
   - Train on k-1 folds
   - Evaluate on 1 fold
3. Average evaluation scores
Advantage: Uses all data for training and evaluation
```

### Stratified K-Fold
```
Maintains class distribution in each fold
Best for: Imbalanced classification
```

### Leave-One-Out (LOO)
```
k = number of samples
Computationally expensive but unbiased
Best for: Very small datasets
```

## Learning Curves

```
Plot 1: Training/Validation Error vs Training Size
- Convergence shows learning
- Gap indicates overfitting
- Parallel lines indicate underfitting (high bias)

Plot 2: Training/Validation Error vs Model Complexity
- Optimal complexity at lowest validation error
- Overfitting: validation >> training error
- Underfitting: both errors high and similar
```

## Overfitting vs Underfitting

| Aspect | Underfitting | Optimal | Overfitting |
|--------|-------------|---------|-----------|
| Training Error | High | Low | Very Low |
| Validation Error | High | Low | High |
| Model Complexity | Too Simple | Balanced | Too Complex |
| Gap | Small | Small | Large |
| Cause | Insufficient capacity | - | Too much capacity |
| Fix | More features/complexity | - | Regularization/simpler model |

## Model Comparison Example

```python
from sklearn.model_selection import cross_validate
from sklearn.metrics import accuracy_score, precision_score, recall_score

models = {
    'Logistic': LogisticRegression(),
    'RF': RandomForestClassifier(),
    'XGBoost': XGBClassifier()
}

metrics = ['accuracy', 'precision', 'recall', 'f1']

for name, model in models.items():
    scores = cross_validate(model, X_train, y_train, cv=5, scoring=metrics)
    print(f"{name}:")
    for metric in metrics:
        print(f"  {metric}: {scores[f'test_{metric}'].mean():.3f}")
```

## Best Practices

- Always use separate test set for final evaluation
- Use cross-validation for robust estimates
- Report multiple metrics, not just accuracy
- Monitor training vs validation curves
- Use appropriate metrics for problem type
- Document evaluation methodology
- Compare against baseline
- Validate on independent held-out data
- Report confidence intervals
- Consider business impact not just metrics

## Metric Selection Guide

| Problem | Primary Metric | Secondary |
|---------|---------------|-----------|
| Balanced Binary | Accuracy | F1-Score |
| Imbalanced Binary | F1-Score | AUC-ROC |
| Multi-class Balanced | Accuracy | Macro F1 |
| Multi-class Imbalanced | Weighted F1 | Macro F1 |
| Regression | RMSE | MAE, R² |
| Ranking | AUC-ROC | NDCG |

## Key Learnings

✓ Single metric insufficient for complete assessment
✓ Validation strategy prevents overoptimistic estimates
✓ Different metrics for different problem types
✓ Learning curves diagnose bias/variance issues
✓ Cross-validation provides robust evaluation
✓ Proper evaluation crucial for production deployment
✓ Baseline comparison important for context
✓ Metrics alone don't guarantee practical success
