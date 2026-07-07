# Model Evaluation

## Overview

This folder contains implementations of **model evaluation techniques** essential for assessing machine learning model performance and ensuring generalization to unseen data.

## Key Concepts

- **Train-Test Split**: Dividing data for unbiased evaluation
- **Performance Metrics**: Quantifying model accuracy
- **Confusion Matrix**: Detailed prediction breakdown
- **Overfitting vs Underfitting**: Identifying model capacity issues
- **Cross-Validation**: Robust evaluation with multiple folds
- **ROC Curves**: Trade-off between true and false positive rates
- **AUC Score**: Area under the ROC curve

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
```

## Key Learning Outcomes

✓ Train-test split concepts and best practices
✓ Classification metrics: Accuracy, Precision, Recall, F1-Score
✓ Regression metrics: MSE, RMSE, MAE, R² Score
✓ Confusion matrix interpretation
✓ ROC curves and AUC score
✓ Cross-validation techniques
✓ Identifying overfitting and underfitting
✓ Hyperparameter tuning for model optimization
✓ Threshold optimization for classification
✓ Learning curves and validation curves

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run notebooks or scripts in this folder
jupyter notebook *.ipynb
```

## Classification Metrics

| Metric | Formula | Best For |
|--------|---------|----------|
| Accuracy | (TP+TN)/(TP+TN+FP+FN) | Balanced data |
| Precision | TP/(TP+FP) | Minimizing false positives |
| Recall | TP/(TP+FN) | Minimizing false negatives |
| F1-Score | 2*(Precision*Recall)/(Precision+Recall) | Imbalanced data |
| AUC-ROC | Area under curve | Probability rankings |

## Regression Metrics

| Metric | Formula | Interpretation |
|--------|---------|-----------------|
| MAE | Σ\|y-ŷ\|/n | Average absolute error |
| MSE | Σ(y-ŷ)²/n | Average squared error |
| RMSE | √(Σ(y-ŷ)²/n) | Root mean squared error |
| R² | 1 - (SS_res/SS_tot) | Proportion of variance explained |

## Confusion Matrix

```
               Predicted
           Positive | Negative
Actual  P | TP      | FN
        N | FP      | TN
```

## Best Practices

- Always use separate test set for final evaluation
- Use stratified splits for imbalanced data
- Report multiple metrics, not just accuracy
- Use cross-validation for robust estimates
- Monitor both training and validation performance
- Plot learning curves to diagnose underfitting/overfitting
- Use appropriate metrics for problem type
- Document evaluation methodology

## Key Learnings

✓ Model evaluation is crucial for real-world deployment
✓ Single metric insufficient for complete assessment
✓ Different metrics for different problem types
✓ Validation strategies prevent overoptimistic estimates
✓ Proper evaluation guides hyperparameter tuning
✓ Critical for building production-ready models
