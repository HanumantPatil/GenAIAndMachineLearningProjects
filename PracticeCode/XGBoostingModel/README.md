# XGBoost Model - Extreme Gradient Boosting

## Overview

This folder contains implementations of **XGBoost (Extreme Gradient Boosting)**, a highly optimized gradient boosting library known for winning machine learning competitions and delivering excellent performance on structured data.

## Key Concepts

- **Gradient Boosting**: Sequential ensemble with residual learning
- **Regularization**: L1 and L2 penalties on tree complexity
- **Column Subsampling**: Feature subsampling for diversity
- **Row Subsampling**: Sample subsampling (stochastic boosting)
- **Approximate Split Finding**: Efficient tree construction
- **Weighted Quantile Sketch**: Handling weighted data
- **Sparsity Awareness**: Efficient missing value handling

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
xgboost
```

## Key Learning Outcomes

✓ XGBoost architecture and principles
✓ Hyperparameter tuning strategies
✓ Regularization parameters (lambda, alpha, gamma)
✓ Learning rate and tree construction
✓ Feature importance from XGBoost
✓ Handling missing values
✓ Early stopping for training efficiency
✓ Cross-validation with XGBoost
✓ Custom loss functions
✓ Model interpretation techniques

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run notebooks or scripts in this folder
jupyter notebook *.ipynb
python *.py
```

## XGBoost Hyperparameters

### Booster Parameters
| Parameter | Description | Default |
|-----------|-------------|---------|
| n_estimators | Number of boosting rounds | 100 |
| learning_rate (eta) | Step size shrinkage | 0.3 |
| max_depth | Maximum tree depth | 6 |
| min_child_weight | Min sum of weights in child | 1 |
| subsample | Row subsampling ratio | 1 |
| colsample_bytree | Column subsampling by tree | 1 |
| gamma | Min loss reduction for split | 0 |

### Regularization Parameters
| Parameter | Description | Default |
|-----------|-------------|---------|
| lambda (reg_lambda) | L2 regularization | 1 |
| alpha (reg_alpha) | L1 regularization | 0 |

## XGBoost Workflow

1. **Data Preparation**: Clean, encode, scale data
2. **Create Dataset**: Use DMatrix or compatible format
3. **Set Parameters**: Configure hyperparameters
4. **Cross-validation**: Validate with cv() or sklearn
5. **Train Model**: Use train() or fit()
6. **Make Predictions**: Generate predictions on test data
7. **Evaluate**: Compute metrics
8. **Optimize**: Tune hyperparameters if needed

## Hyperparameter Tuning Strategy

```
1. Start with default parameters
2. Tune max_depth and min_child_weight
3. Adjust gamma
4. Tune subsample and colsample_bytree
5. Reduce learning_rate and increase n_estimators
6. Fine-tune regularization (lambda, alpha)
7. Use early stopping for efficiency
```

## Feature Importance Methods

### Gain
- Average contribution to loss reduction
- Most intuitive and commonly used

### Split
- Number of times feature used for splitting
- Measures frequency of usage

### Cover
- Average coverage of splits using feature
- Number of samples affected

## Early Stopping Example

```python
params = {'max_depth': 6, 'learning_rate': 0.1}
evals = [(X_test, y_test)]

model = xgb.XGBClassifier(**params)
model.fit(X_train, y_train, 
          eval_set=evals,
          early_stopping_rounds=10,
          verbose=False)
```

## XGBoost vs Other Gradient Boosting

| Aspect | XGBoost | LightGBM | CatBoost |
|--------|---------|----------|----------|
| Speed | Fast | Very Fast | Fast |
| Categorical | Manual encode | Native support | Native support |
| Memory | Moderate | Low | Moderate |
| Parameters | Many | Many | Fewer |
| Accuracy | Excellent | Excellent | Excellent |

## Handling Missing Values

```
XGBoost handles missing values natively:
- Default direction: Left or right child
- Learns optimal direction during training
- No preprocessing needed
```

## Advantages and Disadvantages

**Advantages:**
✓ Excellent performance on structured data
✓ Handles missing values efficiently
✓ Feature importance readily available
✓ Parallel and GPU support
✓ Cross-validation built-in
✓ Regularization prevents overfitting
✓ Predictable performance improvements

**Disadvantages:**
✗ Many hyperparameters to tune
✗ Can be slow with very large datasets
✗ Less interpretable than simpler models
✗ Requires proper hyperparameter tuning
✗ Overkill for simple problems

## Best Practices

- Use early stopping to avoid overfitting
- Start with moderate learning_rate (0.05-0.1)
- Increase n_estimators with small learning_rate
- Use cross-validation for robustness
- Validate on independent test set
- Monitor feature importance for insights
- Consider GPU acceleration for large data
- Document hyperparameter choices
- Compare with simpler baselines
- Use stratified splits for imbalanced data

## Model Evaluation

```python
from sklearn.metrics import classification_report, confusion_matrix
from xgboost import plot_importance

# Predictions
y_pred = model.predict(X_test)

# Metrics
print(classification_report(y_test, y_pred))

# Feature importance
plot_importance(model)
```

## Key Learnings

✓ XGBoost state-of-the-art for structured data
✓ Gradient boosting powerful ensemble method
✓ Proper hyperparameter tuning essential
✓ Regularization controls overfitting
✓ Feature importance provides model insights
✓ Early stopping improves efficiency
✓ Production-ready with robust API
✓ Often outperforms simpler algorithms
