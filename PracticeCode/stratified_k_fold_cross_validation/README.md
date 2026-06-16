# Stratified K-Fold Cross-Validation

## Overview

This folder contains implementations of **Stratified K-Fold Cross-Validation**, a specialized cross-validation technique that maintains class distribution in each fold, making it ideal for imbalanced datasets.

## Key Concepts

- **Stratified Sampling**: Preserving class proportions
- **Imbalanced Data**: Handling unequal class distributions
- **Fold Creation**: Creating representative subsets
- **Bias Prevention**: Avoiding skewed fold distributions
- **Reproducibility**: Consistent results with random_state
- **Multi-label Stratification**: Handling multiple target variables

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
```

## Key Learning Outcomes

✓ When to use Stratified K-Fold vs standard K-Fold
✓ Maintaining class distribution across folds
✓ Implementation with scikit-learn
✓ Impact on evaluation metrics
✓ Hyperparameter tuning with Stratified K-Fold
✓ Handling multi-class problems
✓ Working with time series data considerations
✓ Reproducibility and random seed management
✓ Cross-validation for imbalanced classification

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run notebooks or scripts in this folder
jupyter notebook *.ipynb
python *.py
```

## Stratified vs Standard K-Fold

| Aspect | Standard K-Fold | Stratified K-Fold |
|--------|-----------------|-------------------|
| Class Distribution | May be skewed | Preserved |
| Best For | Balanced data | Imbalanced data |
| Variance in Scores | Higher | Lower |
| Reliability | Good | Better |
| Complexity | Simpler | Slightly complex |

## Example: Class Distribution

**Imbalanced Data: 90% Class 0, 10% Class 1**

**Standard K-Fold (May Result In):**
- Fold 1: 85% Class 0, 15% Class 1 (skewed)
- Fold 2: 95% Class 0, 5% Class 1 (very skewed)

**Stratified K-Fold (Maintains):**
- Each fold: ~90% Class 0, ~10% Class 1 (consistent)

## Implementation

```python
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for train_index, test_index in skf.split(X, y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    # Train and evaluate model
```

## Best Practices

- Always use Stratified K-Fold for imbalanced datasets
- Set random_state for reproducibility
- Use n_splits=5 or 10 for balanced trade-off
- Shuffle data for better randomization
- Perform hyperparameter tuning inside cross-validation
- Report mean and standard deviation of scores
- Use cross_validate for multiple metrics
- Monitor fold-wise score distribution

## Key Learnings

✓ Stratified K-Fold critical for imbalanced data
✓ Provides more reliable performance estimates
✓ Essential for production ML pipelines
✓ Reduces variance in evaluation metrics
✓ Prevents biased model selection
✓ Standard practice in competition and real-world ML
