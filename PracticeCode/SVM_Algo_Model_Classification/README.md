# Support Vector Machine (SVM) - Classification

## Overview

This folder contains implementations of **Support Vector Machine (SVM)**, a powerful supervised learning algorithm for binary and multi-class classification that finds optimal hyperplanes to separate classes.

## Key Concepts

- **Support Vectors**: Critical data points defining decision boundary
- **Hyperplane**: Decision boundary separating classes
- **Margin**: Distance between hyperplane and nearest points
- **Kernel Trick**: Non-linear transformation without explicit computation
- **C Parameter**: Regularization controlling misclassification penalty
- **Gamma**: Influence range of single training example

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
```

## Key Learning Outcomes

✓ SVM fundamentals and geometric interpretation
✓ Linear SVM for linearly separable data
✓ Soft-margin SVM for non-separable data
✓ Kernel methods (Linear, RBF, Polynomial, Sigmoid)
✓ Hyperparameter tuning (C, gamma)
✓ Multi-class classification strategies
✓ Feature scaling importance
✓ Support vector interpretation
✓ Model evaluation for classification
✓ When to use SVM vs other algorithms

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run notebooks or scripts in this folder
jupyter notebook *.ipynb
python *.py
```

## SVM Kernels

| Kernel | Function | Best For |
|--------|----------|----------|
| Linear | κ(x,y) = x·y | Linearly separable data |
| RBF | κ(x,y) = exp(-γ\|\|x-y\|\|²) | Non-linear, complex patterns |
| Polynomial | κ(x,y) = (γx·y+r)^d | Polynomial decision boundaries |
| Sigmoid | κ(x,y) = tanh(γx·y+r) | Similar to neural networks |

## SVM Parameters

**C (Regularization Parameter)**
- Small C: Wider margin, more misclassifications
- Large C: Narrow margin, fewer misclassifications
- Typical range: 0.1 to 1000

**Gamma (Kernel Coefficient)**
- Small γ: Each support vector has far-reaching influence
- Large γ: Each support vector has close influence
- Typical range: 0.001 to 1000

## Mathematical Foundation

**Optimization Problem:**
```
Minimize: (1/2)w^T·w + C·Σξᵢ
Subject to: yᵢ(w^T·φ(xᵢ)+b) >= 1-ξᵢ
```

**Decision Function:**
```
f(x) = sign(Σαᵢyᵢκ(xᵢ,x) + b)
```

## Implementation Steps

1. Data preprocessing and feature scaling
2. Train-test split
3. Model selection (choose kernel)
4. Hyperparameter tuning (C, gamma)
5. Cross-validation for robustness
6. Final model training
7. Evaluation and metrics

## Advantages and Disadvantages

**Advantages:**
✓ Effective in high-dimensional spaces
✓ Memory efficient (uses support vectors)
✓ Versatile through kernel methods
✓ Robust to outliers (with soft margin)

**Disadvantages:**
✗ Slow for large datasets
✗ Difficult to interpret decisions
✗ Requires feature scaling
✗ Hyperparameter tuning can be tedious

## Best Practices

- Standardize/normalize features (essential for SVM)
- Start with RBF kernel for non-linear data
- Use Grid Search or Random Search for hyperparameter tuning
- Apply cross-validation for robustness
- Monitor support vector count
- Use probability calibration for probabilistic output
- Handle imbalanced data with class_weight
- Validate on independent test set

## Model Evaluation Metrics

✓ **Accuracy**: Overall correctness
✓ **Precision**: Positive predictive value
✓ **Recall**: True positive rate
✓ **F1-Score**: Balance of precision and recall
✓ **AUC-ROC**: Discrimination ability
✓ **Confusion Matrix**: Detailed prediction breakdown

## Key Learnings

✓ SVM powerful for classification tasks
✓ Kernel methods enable non-linear classification
✓ Proper scaling crucial for performance
✓ Hyperparameter tuning essential
✓ Strong theoretical foundation
✓ Suitable for medium-sized datasets
✓ Alternative to neural networks for structured data
