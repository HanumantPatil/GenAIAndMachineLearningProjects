# Handle Class Imbalance

## Overview

This folder contains implementations of **techniques to handle class imbalance** in machine learning datasets where one class has significantly more samples than others.

## Contents

- `class_imbalance.ipynb`: Basic techniques for handling class imbalance
- `class_imbalance_imp.ipynb`: Improved implementation with advanced methods
- `churn.csv`: Customer churn dataset with class imbalance

## Key Concepts

- **Class Imbalance**: Unequal distribution of classes
- **Sampling Techniques**: Oversampling and Undersampling
- **SMOTE**: Synthetic Minority Over-sampling Technique
- **Class Weights**: Penalizing minority classes more
- **Evaluation Metrics**: Precision, Recall, F1-Score, AUC-ROC
- **Threshold Optimization**: Adjusting decision boundaries

## Files & Notebooks

### `class_imbalance.ipynb`
- Understanding class imbalance problem
- Data exploration and visualization
- Basic oversampling and undersampling
- Evaluation metrics comparison
- Baseline model performance

### `class_imbalance_imp.ipynb`
- Advanced SMOTE implementation
- Class weight balancing
- Threshold optimization techniques
- Performance metrics: Precision, Recall, F1-Score, AUC-ROC
- Cross-validation strategies for imbalanced data

## Dataset

**churn.csv**: Customer churn classification dataset
- Features: Customer demographics, usage patterns, etc.
- Target: Churn (0/1) - typically imbalanced
- Problem: Predicting customer churn
- Used for: Classification with imbalance

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
imbalanced-learn
```

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run Jupyter notebook
jupyter notebook class_imbalance.ipynb
```

## Techniques Covered

✓ Random Oversampling
✓ Random Undersampling
✓ SMOTE (Synthetic Minority Over-sampling Technique)
✓ ADASYN (Adaptive Synthetic Sampling)
✓ Class Weight Balancing
✓ Threshold Optimization
✓ Cost-sensitive Learning

## Evaluation Metrics for Imbalanced Data

✓ **Precision**: True positives / (True positives + False positives)
✓ **Recall (Sensitivity)**: True positives / (True positives + False negatives)
✓ **F1-Score**: Harmonic mean of Precision and Recall
✓ **AUC-ROC**: Area under Receiver Operating Characteristic curve
✓ **Confusion Matrix**: Complete prediction breakdown

## Key Learnings

✓ Why accuracy is misleading for imbalanced data
✓ When to oversample vs undersample
✓ SMOTE and synthetic data generation
✓ Proper evaluation metrics for imbalanced problems
✓ Cross-validation strategies for imbalance
✓ Business context in handling imbalance
