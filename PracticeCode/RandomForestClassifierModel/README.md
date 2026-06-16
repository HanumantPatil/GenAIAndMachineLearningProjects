# Random Forest Classifier

## Overview

This folder contains implementations of **Random Forest Classifier**, an ensemble learning method that combines multiple decision trees to improve classification performance and reduce overfitting.

## Key Concepts

- **Ensemble Learning**: Combining multiple models for better predictions
- **Bootstrap Aggregating (Bagging)**: Sampling with replacement for diversity
- **Random Feature Selection**: Subset of features at each split
- **Out-of-Bag (OOB) Error**: Estimate without separate test set
- **Feature Importance**: Quantifying feature contributions
- **Parallel Predictions**: Averaging predictions from multiple trees

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
```

## Key Learning Outcomes

✓ Random Forest fundamentals and theory
✓ Bootstrap sampling and aggregation
✓ Random feature selection mechanism
✓ Tree diversity and ensemble effect
✓ Hyperparameter tuning (n_estimators, max_depth, etc.)
✓ Feature importance analysis
✓ Out-of-Bag (OOB) error estimation
✓ Handling imbalanced data
✓ Model evaluation and validation
✓ Comparison with single decision trees

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run notebooks or scripts in this folder
jupyter notebook *.ipynb
python *.py
```

## Random Forest Algorithm

1. **Bootstrap Samples**: Create k samples by sampling with replacement
2. **Build Trees**: For each sample, grow decision tree to full depth
3. **Random Features**: At each split, consider random feature subset
4. **Aggregate**: Average predictions (regression) or vote (classification)
5. **Prediction**: Average (or majority vote) of all tree predictions

## Key Hyperparameters

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| n_estimators | Number of trees | 100-1000 |
| max_depth | Maximum tree depth | 5-30 or None |
| min_samples_split | Samples required to split | 2-20 |
| min_samples_leaf | Samples required at leaf | 1-10 |
| max_features | Features for splitting | 'sqrt', 'log2', None |
| bootstrap | Use bootstrap sampling | True/False |

## Feature Importance Calculation

```
Importance(i) = Σ (gain_i) / total_gains

Where gain_i is the improvement from splits using feature i
across all trees
```

**Relative Importance:** Normalized 0 to 1

## Out-of-Bag (OOB) Error

```
OOB Error = errors on samples not in bootstrap sample
Approximately equals test error (no separate test set needed)
```

**Advantages:**
- Uses training data efficiently
- No need for separate validation set
- Estimates generalization error

## Advantages and Disadvantages

**Advantages:**
✓ Handles both classification and regression
✓ Reduces overfitting compared to single tree
✓ Handles missing values reasonably
✓ Feature importance available
✓ Parallel and scalable
✓ Robust to outliers
✓ Works with mixed feature types

**Disadvantages:**
✗ Less interpretable than single tree
✗ Memory intensive for large data
✗ Slower predictions than single tree
✗ May be slow to train with many trees
✗ Bias towards high-cardinality features

## Best Practices

- Start with n_estimators=100, increase if needed
- Use cross-validation for hyperparameter tuning
- Scale features if using with other algorithms
- Monitor OOB error if available
- Interpret top feature importances
- Validate on independent test set
- Consider class weights for imbalanced data
- Document hyperparameter choices
- Compare with baseline models

## Feature Selection Strategy

1. Train Random Forest
2. Extract feature importances
3. Remove low-importance features
4. Retrain with selected features
5. Compare performance
6. Iterate if needed

## Model Evaluation Metrics

✓ **Accuracy**: Overall correctness
✓ **Precision**: True positive rate
✓ **Recall**: Sensitivity
✓ **F1-Score**: Balance of precision/recall
✓ **AUC-ROC**: Discrimination ability
✓ **Confusion Matrix**: Detailed breakdown
✓ **Cross-validation Score**: Robust estimate

## Key Learnings

✓ Ensemble methods improve individual model performance
✓ Random Forest robust and practical algorithm
✓ Feature importance provides model interpretation
✓ OOB error useful for unbiased evaluation
✓ Hyperparameter tuning significantly affects performance
✓ Gold standard baseline for many problems
✓ Scales to moderately large datasets
