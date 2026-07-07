# Feature Selection

## Overview

This folder contains implementations of **feature selection techniques** used to identify the most relevant features for machine learning models. Feature selection improves model performance, reduces overfitting, and decreases training time.

## Contents

- `feature_selection_using_corr.ipynb`: Feature selection using correlation analysis
- `feature_selection_using_corr_imp.ipynb`: Improved correlation-based feature selection
- `home_prices.csv`: Housing dataset for feature analysis

## Key Concepts

- **Correlation Analysis**: Finding linear relationships between features
- **Correlation Matrix**: Visual representation of feature correlations
- **Multicollinearity**: Problem of highly correlated features
- **Feature Redundancy**: Removing redundant features
- **Feature Relevance**: Selecting features most relevant to target

## Files & Notebooks

### `feature_selection_using_corr.ipynb`
- Correlation matrix computation
- Heatmap visualization
- Identifying highly correlated feature pairs
- Removing redundant features

### `feature_selection_using_corr_imp.ipynb`
- Advanced correlation analysis
- Statistical significance testing
- Multiple feature selection methods comparison
- Performance impact of feature selection

## Dataset

**home_prices.csv**: Housing dataset
- Multiple features: Square footage, bedrooms, bathrooms, etc.
- Target: House prices
- Used for: Regression and feature analysis

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
scipy
```

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run Jupyter notebook
jupyter notebook feature_selection_using_corr.ipynb
```

## Feature Selection Methods Covered

✓ Correlation-based selection
✓ Identifying and removing multicollinearity
✓ Variance Inflation Factor (VIF)
✓ Feature importance ranking
✓ Domain knowledge-based selection
✓ Performance comparison with/without feature selection

## Key Learnings

✓ Why feature selection matters
✓ How to detect multicollinearity
✓ Strategies for removing redundant features
✓ Impact on model performance and interpretability
✓ Computational efficiency gains
