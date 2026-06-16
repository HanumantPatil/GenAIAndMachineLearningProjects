# K-Fold Validation

## Overview

This folder contains implementations of **K-Fold Cross-Validation**, a crucial technique for model evaluation that provides more reliable performance estimates than simple train-test split.

## Key Concepts

- **Cross-Validation**: Dividing data into multiple folds for robust evaluation
- **K-Fold CV**: Split data into k subsets, train on k-1, test on 1
- **Overfitting Detection**: Identifying when model memorizes data
- **Generalization Error**: True performance on unseen data
- **Variance Reduction**: Multiple evaluation rounds reduce variance
- **Stratified K-Fold**: Maintaining class distribution in each fold

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
```

## Key Learning Outcomes

✓ Why K-Fold CV is better than simple train-test split
✓ How to implement K-Fold cross-validation
✓ Choosing appropriate k value
✓ Stratified K-Fold for imbalanced datasets
✓ Cross-validation for hyperparameter tuning
✓ Calculating confidence intervals from CV scores
✓ Detecting overfitting and underfitting
✓ Leave-One-Out Cross-Validation (LOOCV)
✓ Time Series Cross-Validation considerations

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run notebooks or scripts in this folder
jupyter notebook *.ipynb
```

## Cross-Validation Methods

✓ **K-Fold CV**: Equal-sized folds
✓ **Stratified K-Fold**: Preserves class distribution
✓ **Leave-One-Out (LOO)**: k = number of samples
✓ **Time Series Split**: For temporal data
✓ **Shuffle Split**: Random subset selection

## Best Practices

- Use stratified K-Fold for imbalanced data
- Use k=5 or k=10 for balanced trade-off
- Perform hyperparameter tuning inside cross-validation loops
- Report mean and standard deviation of CV scores
- Use cross_validate for multiple metrics simultaneously
- Shuffle data before splitting for better randomization

## Key Learnings

✓ K-Fold CV provides robust performance estimates
✓ Reduces variance in model evaluation
✓ Efficient use of limited data
✓ Better detection of overfitting
✓ Standard practice in ML workflows
✓ Essential for model selection and comparison
