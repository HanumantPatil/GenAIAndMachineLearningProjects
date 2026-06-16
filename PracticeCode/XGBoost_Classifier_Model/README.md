# XGBoost Classifier Model - Binary and Multi-Class Classification

## Overview

This folder contains implementations of **XGBoost Classifier** for both binary and multi-class classification tasks, demonstrating the versatility and effectiveness of XGBoost as a classification algorithm.

## Key Concepts

- **Gradient Boosting for Classification**: Sequential tree boosting
- **Logistic Loss**: Classification-specific loss function
- **Probability Calibration**: Converting scores to probabilities
- **Class Weights**: Handling imbalanced classification
- **ROC-AUC**: Probability ranking evaluation metric
- **Scale_pos_weight**: Imbalanced binary classification parameter

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
xgboost
```

## Key Learning Outcomes

✓ XGBoost for binary classification
✓ XGBoost for multi-class classification
✓ Parameter tuning for classification
✓ Handling imbalanced classes
✓ Probability calibration techniques
✓ ROC curves and AUC score
✓ Feature importance for classification
✓ Threshold optimization
✓ Cross-validation for classification
✓ Model evaluation and interpretation

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run notebooks or scripts in this folder
jupyter notebook *.ipynb
python *.py
```

## XGBoost Classifier Parameters

### Classification-Specific Parameters
| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| objective | Loss function | 'binary:logistic' or 'multi:softmax' | N/A |
| num_class | Number of classes | - | > 2 for multi-class |
| eval_metric | Evaluation metric | 'error' or 'mlogloss' | Various |
| scale_pos_weight | Weight of positive class | 1 | For imbalanced |

## Binary Classification

```python
import xgboost as xgb

# Create classifier
model = xgb.XGBClassifier(
    objective='binary:logistic',
    learning_rate=0.1,
    max_depth=6,
    n_estimators=100,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict probabilities
y_proba = model.predict_proba(X_test)[:, 1]
```

## Multi-Class Classification

```python
# Create classifier
model = xgb.XGBClassifier(
    objective='multi:softmax',
    num_class=3,
    learning_rate=0.1,
    max_depth=6,
    n_estimators=100,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)
```

## Handling Imbalanced Classes

### Method 1: scale_pos_weight
```python
model = xgb.XGBClassifier(
    scale_pos_weight=negative_class_count / positive_class_count
)
```

### Method 2: class_weight
```python
model = xgb.XGBClassifier()
# sklearn interface handles automatically
```

### Method 3: SMOTE Oversampling
```python
from imblearn.over_sampling import SMOTE

smote = SMOTE()
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
model.fit(X_resampled, y_resampled)
```

## Classification Metrics

| Metric | Use Case |
|--------|----------|
| **Accuracy** | Balanced data |
| **Precision** | Minimize false positives |
| **Recall** | Minimize false negatives |
| **F1-Score** | Balance precision/recall |
| **AUC-ROC** | Probability discrimination |
| **Log Loss** | Probability calibration |

## Probability Calibration

```python
from sklearn.calibration import CalibratedClassifierCV

# Calibrate probabilities
calibrated = CalibratedClassifierCV(model, cv=5)
calibrated.fit(X_train, y_train)
y_proba_calibrated = calibrated.predict_proba(X_test)
```

## Feature Importance for Classification

```python
import xgboost as xgb

# Get feature importances
importances = model.get_booster().get_score(importance_type='gain')

# Plot
xgb.plot_importance(model, importance_type='gain')
plt.show()
```

## ROC Curve and AUC

```python
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

# Calculate ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_proba)
roc_auc = auc(fpr, tpr)

# Plot
plt.plot(fpr, tpr, label=f'AUC = {roc_auc:.2f}')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.show()
```

## Threshold Optimization

```python
from sklearn.metrics import precision_recall_curve

# For binary classification, find optimal threshold
precision, recall, thresholds = precision_recall_curve(y_test, y_proba)
f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10)
optimal_threshold = thresholds[np.argmax(f1_scores)]

# Apply threshold
y_pred_optimized = (y_proba >= optimal_threshold).astype(int)
```

## Best Practices

- Use stratified cross-validation
- Monitor both training and validation metrics
- Handle class imbalance explicitly
- Calibrate probabilities for probabilistic output
- Evaluate on independent test set
- Document threshold choices
- Check for class-specific performance
- Use appropriate evaluation metrics
- Consider computational cost
- Validate business impact of predictions

## Confusion Matrix Analysis

```python
from sklearn.metrics import confusion_matrix, classification_report

cm = confusion_matrix(y_test, y_pred)
print(classification_report(y_test, y_pred))
```

## Key Learnings

✓ XGBoost excellent for classification
✓ Handles imbalanced data effectively
✓ Feature importance reveals decision drivers
✓ Proper metric selection crucial
✓ Probability calibration improves reliability
✓ Threshold optimization for specific use cases
✓ Both binary and multi-class supported
✓ Production-ready classification solution
