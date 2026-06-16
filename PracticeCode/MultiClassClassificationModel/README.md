# Multi-Class Classification Model

## Overview

This folder contains implementations of **multi-class classification**, where the target variable has more than two classes, extending binary classification concepts to multiple categories.

## Key Concepts

- **Multi-class Classification**: Predicting one of k>2 classes
- **One-vs-Rest (OvR)**: Train k binary classifiers
- **One-vs-One (OvO)**: Train k(k-1)/2 binary classifiers
- **Multinomial Classification**: Native multi-class support
- **Class Imbalance**: Unequal class distributions
- **Performance Metrics**: Extending binary metrics to multi-class

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
```

## Key Learning Outcomes

✓ Multi-class classification strategies
✓ One-vs-Rest (OvR) vs One-vs-One (OvO)
✓ Algorithms with native multi-class support
✓ Class probability calibration
✓ Confusion matrix for multi-class
✓ Multi-class metrics (macro, micro, weighted averages)
✓ Handling class imbalance
✓ Cross-validation for multi-class
✓ Feature importance interpretation
✓ Threshold adjustment strategies

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run notebooks or scripts in this folder
jupyter notebook *.ipynb
python *.py
```

## Multi-class Strategies

### One-vs-Rest (OvR/One-vs-All)
```
For k classes, train k binary classifiers
- Classifier 1: Class 1 vs Rest (classes 2,3,...,k)
- Classifier 2: Class 2 vs Rest (classes 1,3,...,k)
- Prediction: Argmax of decision scores
```

### One-vs-One (OvO)
```
For k classes, train k(k-1)/2 binary classifiers
- Classifier 1: Class 1 vs Class 2
- Classifier 2: Class 1 vs Class 3
- ...and so on
Prediction: Majority vote or argmax
```

## Algorithm Comparison

| Algorithm | Native Multi-class | Strategy |
|-----------|-------------------|----------|
| Logistic Regression | Yes | Multinomial |
| SVM | No (OvR by default) | OvO supported |
| Random Forest | Yes | Multinomial |
| Naive Bayes | Yes | Multinomial |
| KNN | Yes | Native |
| Decision Tree | Yes | Native |
| Gradient Boosting | Yes | Native |

## Multi-class Metrics

### Precision, Recall, F1-Score

**Macro Average** (unweighted mean per class):
```
Macro_Precision = (Precision_1 + Precision_2 + ... + Precision_k) / k
```

**Micro Average** (aggregate all TP, FP, FN):
```
Micro_Precision = Total_TP / (Total_TP + Total_FP)
```

**Weighted Average** (by class support):
```
Weighted_Precision = Σ(Precision_i × support_i) / total_support
```

## Confusion Matrix for Multi-Class

```
Example 3-class (A, B, C):
        Predicted
        A   B   C
Actual A | 45  3  2
       B |  1  50  4
       C |  2  3  45
```

**Per-class Metrics:**
- Class A: TP=45, FN=5 (3+2), FP=3 (1+2)
- Class B: TP=50, FN=5 (1+4), FP=6 (3+3)
- Class C: TP=45, FN=6 (2+4), FP=5 (2+3)

## Handling Class Imbalance

| Technique | Description |
|-----------|-------------|
| Class Weights | Penalize minority classes more |
| Stratified K-Fold | Maintain distribution in folds |
| SMOTE | Generate synthetic minority samples |
| Cost-sensitive Learning | Different misclassification costs |
| Ensemble Methods | Combine predictions from multiple models |

## Best Practices

- Use stratified cross-validation
- Report macro and weighted averages
- Check confusion matrix for common confusions
- Use appropriate metrics for business problem
- Handle class imbalance explicitly
- Monitor per-class performance
- Consider class costs (some errors more costly)
- Balance precision/recall based on use case
- Validate on independent test set
- Document class definitions clearly

## Example Metrics Computation

```python
from sklearn.metrics import classification_report, confusion_matrix

# Assume y_true, y_pred are actual and predicted labels

# Detailed report
print(classification_report(y_true, y_pred))

# Confusion matrix
cm = confusion_matrix(y_true, y_pred)

# Per-class metrics
from sklearn.metrics import precision_recall_fscore_support
prec, recall, f1, support = precision_recall_fscore_support(y_true, y_pred)
```

## Real-World Examples

- **Email classification**: Spam, Promotional, Updates, Social, Primary
- **Document categorization**: News, Sports, Politics, Technology, Entertainment
- **Sentiment analysis**: Positive, Neutral, Negative
- **Product classification**: Electronics, Clothing, Food, Books, etc.

## Key Learnings

✓ Multi-class extends binary classification concepts
✓ Different strategies for different algorithms
✓ Proper metric selection crucial
✓ Class imbalance common in multi-class
✓ Confusion matrix shows specific confusions
✓ Per-class analysis reveals strengths/weaknesses
✓ Business context drives metric choices
✓ Production systems often use ensemble methods
