# Hyperparameter Tuning - Grid Search Cross-Validation

## Overview

This folder contains implementations of **Grid Search with Cross-Validation**, a systematic approach to hyperparameter tuning that exhaustively searches over specified parameter values.

## Key Concepts

- **Hyperparameters**: Parameters set before training (not learned)
- **Grid Search**: Exhaustive search over parameter grid
- **Cross-Validation**: Robust evaluation during tuning
- **Best Parameters**: Optimal configuration selection
- **Computational Cost**: Trading time for accuracy
- **Parameter Space**: Defining search boundaries

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
```

## Key Learning Outcomes

✓ Hyperparameter vs Model Parameters distinction
✓ Grid Search implementation and execution
✓ Parameter grid definition
✓ Cross-validation integration with Grid Search
✓ Performance metrics for parameter selection
✓ Analyzing grid search results
✓ Parallel execution (n_jobs)
✓ Best parameters extraction
✓ Comparison with Random Search
✓ Fine-tuning after initial Grid Search

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run notebooks or scripts in this folder
jupyter notebook *.ipynb
python *.py
```

## Grid Search Process

1. Define parameter grid (ranges for each hyperparameter)
2. Create model and Grid Search object
3. Fit Grid Search on training data
4. Extract best parameters
5. Train final model with best parameters
6. Evaluate on test set

## Grid Search Example

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(
    estimator=RandomForestClassifier(),
    param_grid=param_grid,
    cv=5,
    n_jobs=-1
)

grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_
```

## Grid Search vs Random Search

| Aspect | Grid Search | Random Search |
|--------|-----------|--------------|
| Coverage | All combinations | Random sample |
| Completeness | Exhaustive | Probabilistic |
| Time | Slower | Faster |
| Performance | Guaranteed best in grid | May miss better params |
| High-dim | Inefficient | More efficient |

## Best Practices

- Start with coarse grid, then refine
- Use parallel execution (n_jobs=-1)
- Specify realistic parameter ranges
- Use cross-validation (cv=5 or cv=10)
- Monitor computational resources
- Document parameter importance
- Save best model and parameters
- Validate on held-out test set
- Consider Random Search for large spaces

## Common Hyperparameters by Algorithm

**Tree-based Models:**
- max_depth, min_samples_split, min_samples_leaf, n_estimators

**Regularization:**
- C (inverse), alpha (regularization strength), penalty (L1/L2)

**SVM:**
- C (regularization), kernel, gamma (RBF kernel)

**Neural Networks:**
- learning_rate, batch_size, hidden_layer_sizes, activation

## Key Learnings

✓ Systematic hyperparameter optimization improves performance
✓ Grid Search ensures exhaustive exploration
✓ Cross-validation prevents overfitting to test set
✓ Computational cost-benefit analysis important
✓ Parameter ranges significantly impact results
✓ Essential for production model development
✓ Complements domain knowledge and theory
