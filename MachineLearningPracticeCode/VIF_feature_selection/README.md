# VIF Feature Selection - Variance Inflation Factor

## Overview

This folder contains implementations of **Variance Inflation Factor (VIF)** analysis, a statistical technique to detect and remove multicollinearity (high correlation) among features in regression models.

## Key Concepts

- **Multicollinearity**: High correlation between independent variables
- **Variance Inflation Factor (VIF)**: Quantifies multicollinearity severity
- **Feature Redundancy**: Correlated features provide redundant information
- **Model Stability**: Multicollinearity reduces model stability
- **Coefficient Interpretation**: Unreliable estimates with multicollinearity
- **Feature Importance**: Impact on identifying truly important features

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
statsmodels
```

## Key Learning Outcomes

✓ Understanding multicollinearity problem
✓ VIF calculation and interpretation
✓ VIF thresholds and decision-making
✓ Iterative VIF-based feature selection
✓ Impact on model performance
✓ Alternative detection methods (correlation matrix)
✓ Handling multicollinearity strategies
✓ Regression model stability improvement
✓ Coefficient interpretation with/without multicollinearity

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run notebooks or scripts in this folder
jupyter notebook *.ipynb
python *.py
```

## VIF Interpretation

| VIF Value | Multicollinearity | Action |
|-----------|-------------------|--------|
| 1 | None | Keep feature |
| 1-5 | Low to Moderate | Keep (depends on context) |
| 5-10 | Moderate to High | Consider removing |
| > 10 | High (Problem) | Remove feature |

## VIF Calculation

```
VIF(Xᵢ) = 1 / (1 - Rᵢ²)

Where Rᵢ² is the R-squared from regressing Xᵢ on other features
```

**Interpretation:**
- VIF = 1: No correlation with other features
- VIF = 5: Variable explains 80% of variance with others
- VIF > 10: Severe multicollinearity

## Feature Selection Process

1. Calculate VIF for all features
2. Identify features with VIF > threshold (typically 10 or 5)
3. Remove feature with highest VIF
4. Recalculate VIF for remaining features
5. Repeat until all VIFs below threshold

## Multicollinearity Strategies

✓ Remove redundant features (VIF-based)
✓ Principal Component Analysis (PCA)
✓ Regularization (Ridge/Lasso)
✓ Domain knowledge-based selection
✓ Combine correlated features
✓ Collect more data to disambiguate

## Best Practices

- Calculate VIF for all numeric features
- Use domain knowledge to inform decisions
- Don't remove important features just for low VIF
- Consider business context and interpretability
- Apply feature scaling before VIF calculation
- Document removed features and reasoning
- Validate improved model performance
- Monitor coefficient stability

## Key Learnings

✓ Multicollinearity seriously impacts regression
✓ VIF provides quantitative multicollinearity measure
✓ Systematic feature selection approach
✓ Improves model stability and interpretability
✓ Essential preprocessing for regression models
✓ Complements correlation analysis
✓ Critical for production ML pipelines
