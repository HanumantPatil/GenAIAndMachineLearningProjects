# L1 & L2 Regularization

## Overview

This folder contains implementations of **L1 (Lasso) and L2 (Ridge) Regularization** techniques used to prevent overfitting in machine learning models by adding penalty terms to the loss function.

## Key Concepts

- **L1 Regularization (Lasso)**: Adds sum of absolute values of coefficients
- **L2 Regularization (Ridge)**: Adds sum of squared coefficients
- **Elastic Net**: Combination of L1 and L2 regularization
- **Regularization Parameter (λ)**: Controls strength of penalty
- **Feature Selection**: L1 performs implicit feature selection
- **Coefficient Shrinkage**: L2 shrinks coefficients towards zero

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
```

## Key Learning Outcomes

✓ Understanding overfitting problem
✓ How L1 and L2 regularization work
✓ Feature selection via L1 regularization
✓ Coefficient shrinkage via L2 regularization
✓ Elastic Net as hybrid approach
✓ Hyperparameter tuning (λ, α)
✓ Cross-validation for regularization strength
✓ Interpreting regularized models
✓ When to use L1 vs L2 vs Elastic Net

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run notebooks or scripts in this folder
jupyter notebook *.ipynb
```

## Regularization Methods Comparison

| Aspect | L1 (Lasso) | L2 (Ridge) | Elastic Net |
|--------|-----------|-----------|-----------|
| Penalty | Σ\|w\| | Σw² | α*Σ\|w\| + (1-α)*Σw² |
| Feature Selection | Yes (zeros) | No | Yes (partial) |
| Computation | Harder | Easier | Moderate |
| Use Case | Few important features | All features useful | Balance needed |

## Model Equations

**L1 Regularization (Lasso)**
```
Loss = MSE + λ * Σ|coefficients|
```

**L2 Regularization (Ridge)**
```
Loss = MSE + λ * Σ(coefficients²)
```

**Elastic Net**
```
Loss = MSE + λ * (α * Σ|coefficients| + (1-α) * Σ(coefficients²))
```

## Best Practices

- Standardize features before regularization
- Use cross-validation to select λ
- L1 for high-dimensional data with feature selection needs
- L2 for stable predictions with all features
- Elastic Net for balanced approach
- Monitor train vs validation performance
- Interpret coefficients carefully after regularization

## Key Learnings

✓ Regularization prevents overfitting
✓ L1 enables automatic feature selection
✓ L2 provides stable, continuous predictions
✓ Elastic Net combines benefits of both
✓ Parameter tuning crucial for performance
✓ Essential technique in production ML
