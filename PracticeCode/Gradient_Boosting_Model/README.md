# Gradient Boosting Model - Ad Spend Prediction

## Overview

This folder contains implementations of **Gradient Boosting** for regression tasks, specifically predicting ad spending based on marketing features.

## Contents

- `gradient_boosting_ad_spend.ipynb`: Gradient Boosting for ad spend regression
- `gradient_boosting_ad_spend_imp.ipynb`: Improved implementation with optimization
- `ad_spend.csv`: Ad spending dataset

## Key Concepts

- **Gradient Boosting Regressor**: Sequential ensemble for regression
- **Learning Rate**: Control step size in boosting process
- **Number of Estimators**: Number of boosting stages
- **Tree Depth**: Controlling model complexity
- **Residual Fitting**: Learning from prediction errors

## Files & Notebooks

### `gradient_boosting_ad_spend.ipynb`
- Basic Gradient Boosting Regressor implementation
- Data exploration and visualization
- Model training and prediction
- Performance evaluation (MSE, RMSE, R² score)

### `gradient_boosting_ad_spend_imp.ipynb`
- Hyperparameter tuning (learning_rate, n_estimators, max_depth)
- Cross-validation for robust evaluation
- Feature importance analysis
- Prediction accuracy improvement strategies

## Dataset

**ad_spend.csv**: Ad spending regression dataset
- Features: Marketing channels, budget allocation, etc.
- Target: Ad spend amount
- Used for: Regression and predictive modeling

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
```

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run Jupyter notebook
jupyter notebook gradient_boosting_ad_spend.ipynb
```

## Key Learnings

✓ Gradient Boosting for regression tasks
✓ Hyperparameter tuning strategies
✓ Feature importance in boosting models
✓ Overfitting prevention techniques
✓ Cross-validation for model validation
✓ Performance metrics for regression (MSE, RMSE, R²)
