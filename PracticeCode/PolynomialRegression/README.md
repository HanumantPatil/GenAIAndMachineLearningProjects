# Polynomial Regression

## Overview

This folder contains implementations of **Polynomial Regression**, a technique for fitting non-linear relationships between features and target variables by using polynomial features.

## Key Concepts

- **Linear vs Non-linear**: Fitting curved relationships
- **Polynomial Features**: Higher-degree terms (x², x³, etc.)
- **Degree Selection**: Balancing fit and overfitting
- **Bias-Variance Trade-off**: Model complexity considerations
- **Feature Engineering**: Creating polynomial terms
- **Overfitting Risk**: Higher degree polynomials prone to overfitting

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
```

## Key Learning Outcomes

✓ Non-linear regression concepts
✓ Polynomial feature creation and transformation
✓ Selecting optimal polynomial degree
✓ Visualization of polynomial fits
✓ Overfitting and underfitting detection
✓ Cross-validation for degree selection
✓ Regularization to control overfitting
✓ Prediction on new data
✓ Model evaluation metrics (MSE, RMSE, R²)
✓ Comparison with linear models

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run notebooks or scripts in this folder
jupyter notebook *.ipynb
python *.py
```

## Polynomial Regression Model

**Degree 1 (Linear)**
```
y = β₀ + β₁*x
```

**Degree 2 (Quadratic)**
```
y = β₀ + β₁*x + β₂*x²
```

**Degree n**
```
y = β₀ + β₁*x + β₂*x² + ... + βₙ*xⁿ
```

## Degree Selection

| Degree | Characteristics | Use Case |
|--------|-----------------|----------|
| 1 | Linear, simple | Simple relationships |
| 2-3 | Moderate complexity | Most real-world data |
| 4-5 | High complexity | Complex patterns |
| 6+ | Very high complexity | Risk of overfitting |

## Best Practices

- Start with degree 2 or 3, then adjust
- Use cross-validation for degree selection
- Standardize features before fitting
- Apply regularization (Ridge/Lasso) for high degrees
- Visualize predictions against actual data
- Check residuals for patterns
- Monitor train vs validation performance
- Document chosen degree and rationale

## Key Learnings

✓ When to use polynomial regression
✓ Feature engineering for non-linear relationships
✓ Avoiding overfitting with high-degree polynomials
✓ Proper model selection techniques
✓ Performance metrics for regression
✓ Trade-off between flexibility and generalization
✓ Foundation for kernel methods and non-linear techniques
