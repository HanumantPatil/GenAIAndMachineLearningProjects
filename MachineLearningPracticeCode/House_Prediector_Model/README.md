# House Price Predictor Model - Regression

## Overview

This folder contains implementations of **house price prediction**, a fundamental regression problem demonstrating end-to-end machine learning workflows including data exploration, feature engineering, model building, and evaluation.

## Key Concepts

- **Regression**: Predicting continuous target variable
- **Feature Engineering**: Creating meaningful features from raw data
- **Feature Scaling**: Normalizing feature ranges
- **Model Selection**: Choosing appropriate algorithms
- **Hyperparameter Tuning**: Optimizing model parameters
- **Cross-Validation**: Robust performance estimation

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
```

## Key Learning Outcomes

✓ End-to-end regression workflow
✓ Exploratory data analysis (EDA) techniques
✓ Feature engineering and selection
✓ Linear and non-linear regression models
✓ Hyperparameter tuning for regression
✓ Cross-validation strategies
✓ Regression evaluation metrics (MSE, RMSE, R²)
✓ Residual analysis for model diagnostics
✓ Handling outliers and missing values
✓ Model comparison and selection

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run notebooks or scripts in this folder
jupyter notebook *.ipynb
python *.py
```

## Regression Workflow

1. **Load Data**: Load house price dataset
2. **Exploratory Analysis**: Understand data distribution
3. **Data Preprocessing**: Handle missing values, outliers
4. **Feature Engineering**: Create meaningful features
5. **Feature Scaling**: Normalize features
6. **Model Selection**: Choose regression models
7. **Train Models**: Fit models on training data
8. **Hyperparameter Tuning**: Optimize parameters
9. **Evaluation**: Assess performance on test set
10. **Interpretation**: Understand predictions

## Common House Price Features

| Feature | Type | Description |
|---------|------|-------------|
| Square Footage | Numerical | House area |
| Bedrooms | Numerical | Number of bedrooms |
| Bathrooms | Numerical | Number of bathrooms |
| Location | Categorical | Neighborhood/zip code |
| Age | Numerical | House age (years) |
| Lot Size | Numerical | Property size |
| Garage | Numerical | Number of garage spaces |
| Condition | Categorical | Property condition |

## Regression Models Compared

| Model | Complexity | Interpretability | Use Case |
|-------|-----------|-----------------|----------|
| Linear Regression | Low | High | Baseline |
| Polynomial Regression | Medium | Medium | Non-linear relationships |
| Ridge Regression | Medium | High | Feature correlation |
| Lasso Regression | Medium | High | Feature selection |
| Random Forest | High | Medium | Complex patterns |
| Gradient Boosting | High | Medium | Best performance |
| SVM | High | Low | Non-linear data |

## Regression Evaluation Metrics

| Metric | Formula | Interpretation |
|--------|---------|-----------------|
| MAE | Σ\|y-ŷ\|/n | Average absolute error |
| MSE | Σ(y-ŷ)²/n | Average squared error |
| RMSE | √MSE | Root mean squared error (same units as y) |
| R² | 1 - (SS_res/SS_tot) | Proportion of variance explained (0-1) |
| MAPE | Σ\|y-ŷ\|/y/n | Mean absolute percentage error |

## Feature Engineering Techniques

```python
# Interaction features
df['total_rooms'] = df['bedrooms'] + df['bathrooms']
df['price_per_sqft'] = df['price'] / df['sqft']

# Polynomial features
df['sqft_squared'] = df['sqft'] ** 2

# Binning
df['age_category'] = pd.cut(df['age'], bins=[0, 10, 25, 50, 100])

# Log transformation (for skewed distributions)
df['log_price'] = np.log(df['price'])
```

## Residual Analysis

```python
residuals = y_test - y_pred

# Check for patterns
plt.scatter(y_pred, residuals)
plt.axhline(y=0, color='r', linestyle='--')

# Should be:
# - Randomly scattered around 0
# - No pattern or trend
# - Roughly symmetric
```

## Model Comparison Example

```python
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

models = {
    'Linear': LinearRegression(),
    'Random Forest': RandomForestRegressor(),
    'Gradient Boosting': GradientBoostingRegressor()
}

for name, model in models.items():
    model.fit(X_train, y_train)
    r2 = model.score(X_test, y_test)
    print(f'{name}: R² = {r2:.4f}')
```

## Best Practices

- Explore data thoroughly before modeling
- Handle outliers appropriately
- Scale features for better convergence
- Use cross-validation for robust evaluation
- Try multiple models and compare
- Feature engineering often more important than model
- Monitor train vs validation performance
- Interpret model coefficients when possible
- Validate on truly independent test set
- Document assumptions and decisions

## Real-World Considerations

- **Market Trends**: Prices change over time
- **Location Variation**: Significant price variance by area
- **Data Quality**: Missing values, outliers common
- **Feature Relevance**: Feature importance reveals drivers
- **Regulation**: Local laws affect prices
- **Interpretability**: Stakeholders need explanations

## Key Learnings

✓ Regression predicts continuous variables
✓ Feature engineering crucial for performance
✓ Multiple models should be compared
✓ Proper evaluation prevents overoptimism
✓ Interpretability helps stakeholder trust
✓ Practical ML requires data preprocessing
✓ No one-size-fits-all solution
✓ Domain knowledge valuable for feature creation
