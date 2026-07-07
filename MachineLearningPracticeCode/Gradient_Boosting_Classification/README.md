# Gradient Boosting Classification - Titanic Survival Prediction

## Overview

This folder contains implementations of **Gradient Boosting** algorithms for classification tasks, using the famous Titanic survival prediction dataset.

## Contents

- `random_forest_titanic_survival.ipynb`: Random Forest and Gradient Boosting implementations
- `random_forest_titanic_survival_imp.ipynb`: Improved implementations with optimization
- `titanic.csv`: Titanic passenger dataset

## Key Concepts

- **Gradient Boosting**: Ensemble method building models sequentially
- **Weak Learners**: Decision trees that are better than random guessing
- **Residual Learning**: Learning from previous model's errors
- **Loss Functions**: Measuring prediction errors
- **Regularization**: Preventing overfitting in boosting

## Files & Notebooks

### `random_forest_titanic_survival.ipynb`
- Random Forest implementation
- Gradient Boosting implementation
- Data preprocessing and feature engineering
- Model comparison and evaluation

### `random_forest_titanic_survival_imp.ipynb`
- Optimized Gradient Boosting with hyperparameter tuning
- Cross-validation and performance metrics
- Feature importance analysis
- Prediction on test set

## Dataset

**titanic.csv**: Titanic passenger survival data
- Features: Age, Sex, Pclass, Fare, Embarked, etc.
- Target: Survived (0/1)
- Missing values: Handled through preprocessing
- Used for: Binary classification

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
jupyter notebook random_forest_titanic_survival.ipynb
```

## Models Compared

✓ Random Forest Classifier
✓ Gradient Boosting Classifier
✓ XGBoost (optional)
✓ Performance metrics: Accuracy, Precision, Recall, F1-Score

## Key Learnings

✓ Ensemble methods and their advantages
✓ How Gradient Boosting builds upon weak learners
✓ Feature engineering for classification
✓ Model evaluation and hyperparameter tuning
✓ Handling class imbalance if present
✓ Feature importance interpretation
