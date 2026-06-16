# Hyperparameter Tuning - Randomized Search Cross-Validation

## Overview

This folder contains implementations of **Randomized Search with Cross-Validation**, an efficient alternative to Grid Search for hyperparameter tuning that samples random parameter combinations.

## Key Concepts

- **Randomized Search**: Random sampling from parameter distributions
- **Efficiency**: Faster than exhaustive Grid Search
- **High-Dimensional Spaces**: Better for large parameter spaces
- **Parameter Distributions**: Continuous and discrete distributions
- **Cross-Validation**: Robust evaluation with random sampling
- **Trade-off**: Speed vs Completeness

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

✓ When to use Randomized Search vs Grid Search
✓ Parameter distribution definition (uniform, log-uniform, etc.)
✓ Randomized Search implementation
✓ Cross-validation integration
✓ Sample size and probability of finding best parameters
✓ Parallel execution for efficiency
✓ Comparing results with Grid Search
✓ Warm-start and iterative refinement
✓ Analyzing high-dimensional parameter spaces
✓ Resource-constrained tuning

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run notebooks or scripts in this folder
jupyter notebook *.ipynb
python *.py
```

## Randomized Search Process

1. Define parameter distributions (not grids)
2. Create model and RandomizedSearchCV object
3. Set n_iter (number of combinations to try)
4. Fit RandomizedSearchCV on training data
5. Extract best parameters
6. Train final model with best parameters
7. Evaluate on test set

## RandomizedSearchCV Example

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform, randint

param_dist = {
    'n_estimators': randint(100, 500),
    'max_depth': randint(5, 30),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10),
    'learning_rate': uniform(0.01, 0.3)
}

random_search = RandomizedSearchCV(
    estimator=GradientBoostingClassifier(),
    param_distributions=param_dist,
    n_iter=50,
    cv=5,
    n_jobs=-1,
    random_state=42
)

random_search.fit(X_train, y_train)
```

## Parameter Distributions

| Type | Example | Use Case |
|------|---------|----------|
| Integer | randint(1, 100) | Discrete values (depth, samples) |
| Uniform | uniform(0.1, 1.0) | Continuous range |
| Log-Uniform | loguniform(0.001, 1.0) | Exponential scale (learning rate) |
| List | ['linear', 'rbf', 'poly'] | Categorical choices |

## Grid Search vs Randomized Search

| Aspect | Grid Search | Randomized Search |
|--------|-----------|-------------------|
| Coverage | Exhaustive | Probabilistic |
| Time | O(grid_size) | O(n_iter) |
| Space | Small to medium | Large (ideal) |
| Guarantee | Finds best in grid | Probability-based |
| Learning Rate | Linear, categorical | Continuous ranges |
| Resource Use | High for large spaces | Controlled by n_iter |

## Best Practices

- Use log-uniform for exponential parameters
- Set random_state for reproducibility
- n_iter = 10 * n_params (rough guideline)
- Use parallel execution (n_jobs=-1)
- Define realistic parameter ranges
- Apply log scale for parameters spanning orders of magnitude
- Save best parameters and scores
- Visualize parameter importance
- Refine distributions based on results
- Validate on held-out test set

## When to Use Each Method

**Grid Search:**
- Small parameter space (<= 100 combinations)
- Known parameter ranges
- Categorical parameters
- Need exhaustive guarantee

**Randomized Search:**
- Large parameter space (> 100 combinations)
- High-dimensional spaces
- Continuous parameter distributions
- Resource-constrained environments
- Unknown ideal parameter ranges

## Key Learnings

✓ Randomized Search efficient for large spaces
✓ Covers more ground with fewer evaluations
✓ Probability of finding good parameters
✓ Better for continuous parameter distributions
✓ Complements Grid Search for different scenarios
✓ Essential for resource-efficient tuning
✓ Part of modern ML pipeline best practices
