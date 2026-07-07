# One-Hot Encoding

## Overview

This folder contains implementations of **One-Hot Encoding**, a fundamental technique for converting categorical variables into numerical format suitable for machine learning algorithms.

## Key Concepts

- **Categorical Variables**: Non-numeric features (colors, categories, etc.)
- **One-Hot Encoding**: Binary vectors for each category
- **Dummy Variables**: Representation of categories
- **Feature Engineering**: Preparing data for algorithms
- **Curse of Dimensionality**: Impact on model complexity
- **Ordinal vs Nominal**: Different encoding strategies

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
```

## Key Learning Outcomes

✓ Why categorical encoding is necessary
✓ One-Hot Encoding process and implementation
✓ Dummy Variable Trap and how to avoid it
✓ Multi-categorical variables handling
✓ Performance impact on model complexity
✓ Alternative encoding methods (Label Encoding, Target Encoding)
✓ Handling unknown categories in production
✓ Sparse matrix optimization
✓ Feature scaling after encoding

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run notebooks or scripts in this folder
jupyter notebook *.ipynb
```

## One-Hot Encoding Example

**Before (Categorical)**
```
Color
Red
Blue
Green
Red
```

**After (One-Hot Encoded)**
```
Color_Red  Color_Blue  Color_Green
1          0           0
0          1           0
0          0           1
1          0           0
```

## Encoding Methods Comparison

| Method | Use Case | Drawback |
|--------|----------|----------|
| One-Hot | Nominal categories | Creates many features |
| Label Encoding | Ordinal categories | Implies ordering in nominal |
| Target Encoding | High-cardinality | Risk of overfitting |
| Binary Encoding | High-cardinality | Harder to interpret |

## Implementation Techniques

✓ **pandas.get_dummies()**: Simple implementation
✓ **sklearn.preprocessing.OneHotEncoder**: Production-ready
✓ **Sparse matrices**: Memory-efficient storage
✓ **Handling unknown categories**: Test-time scenarios

## Best Practices

- Drop one category per variable to avoid multicollinearity
- Handle rare categories by grouping them
- Use sparse matrices for high-dimensional data
- Save encoder object for production deployment
- Test with same categories as training data
- Monitor dimensionality explosion
- Consider performance impact on training time

## Key Learnings

✓ One-Hot Encoding essential for categorical data
✓ Dummy Variable Trap must be avoided
✓ Proper preparation improves model performance
✓ Feature dimensionality trade-offs
✓ Essential preprocessing step in ML pipelines
✓ Must handle encoding in both training and production
