# Decision Tree Model - Classification

## Overview

This folder contains implementations of **Decision Tree** algorithms for classification tasks. Decision trees are interpretable models that make predictions by recursively splitting data based on feature values.

## Contents

- `9_decision_tree_salary_classification.ipynb`: Decision tree for salary classification
- `9_decision_tree_salary_classification_imp.ipynb`: Improved implementation with optimizations
- `salaries.csv`: Salary dataset for classification

## Key Concepts

- **Decision Trees**: Tree-like model of decisions and their consequences
- **Splitting**: Information gain, Gini impurity, Entropy
- **Leaf Nodes**: Terminal nodes with predictions
- **Tree Depth**: Control overfitting through depth constraints
- **Feature Importance**: Understanding which features drive predictions

## Files & Notebooks

### `9_decision_tree_salary_classification.ipynb`
- Basic decision tree implementation
- Tree visualization and interpretation
- Feature importance analysis
- Prediction on test data

### `9_decision_tree_salary_classification_imp.ipynb`
- Optimized decision tree with hyperparameter tuning
- Pruning strategies to reduce overfitting
- Cross-validation and performance metrics
- Model comparison with baseline

## Dataset

**salaries.csv**: Salary classification dataset
- Features: Experience, education, skills, etc.
- Target: Salary level (Low/Medium/High)
- Used for: Binary or multi-class classification

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
jupyter notebook 9_decision_tree_salary_classification.ipynb
```

## Key Learnings

✓ How decision trees make splits
✓ Information gain and entropy concepts
✓ Tree depth and overfitting prevention
✓ Feature importance interpretation
✓ Pros and cons of decision trees
✓ When to use decision trees vs other algorithms
