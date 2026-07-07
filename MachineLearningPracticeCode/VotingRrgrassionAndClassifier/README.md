# Voting Regression and Classifier - Ensemble Methods

## Overview

This folder contains implementations of **Voting Ensemble methods**, where multiple diverse models combine their predictions through voting (for classification) or averaging (for regression) to improve overall performance.

## Key Concepts

- **Ensemble Methods**: Combining multiple models
- **Voting Classification**: Majority vote for classification
- **Voting Regression**: Averaging predictions for regression
- **Model Diversity**: Different algorithms for robustness
- **Weighted Voting**: Giving more weight to better models
- **Hard vs Soft Voting**: Direct prediction vs probability-based

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
```

## Key Learning Outcomes

✓ Ensemble learning principles and advantages
✓ Voting Classifier implementation
✓ Voting Regressor implementation
✓ Hard vs Soft voting strategies
✓ Weighted voting for model importance
✓ Model diversity selection
✓ Performance improvement through ensembles
✓ Computational trade-offs
✓ Hyperparameter optimization for ensembles
✓ Comparing individual vs ensemble performance

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run notebooks or scripts in this folder
jupyter notebook *.ipynb
python *.py
```

## Voting Classification

### Hard Voting
```python
from sklearn.ensemble import VotingClassifier

# Create individual classifiers
lr = LogisticRegression()
rf = RandomForestClassifier()
svm = SVC()

# Create voting classifier
vc = VotingClassifier(
    estimators=[('lr', lr), ('rf', rf), ('svm', svm)],
    voting='hard'  # Majority vote
)

vc.fit(X_train, y_train)
predictions = vc.predict(X_test)
```

**Hard Voting Process:**
```
Classifier 1: Predicts Class A
Classifier 2: Predicts Class B
Classifier 3: Predicts Class A
Result: Class A (majority: 2 votes)
```

### Soft Voting
```python
# Create voting classifier with probabilities
vc = VotingClassifier(
    estimators=[('lr', lr), ('rf', rf), ('svm', svm_prob)],
    voting='soft'  # Probability-based averaging
)

# Soft voting averages predicted probabilities
```

**Soft Voting Process:**
```
Classifier 1: [0.8, 0.2] (80% A, 20% B)
Classifier 2: [0.6, 0.4] (60% A, 40% B)
Classifier 3: [0.7, 0.3] (70% A, 30% B)
Average:      [0.7, 0.3] → Predict Class A
```

## Voting Regression

```python
from sklearn.ensemble import VotingRegressor

# Create individual regressors
lr = LinearRegression()
rf = RandomForestRegressor()
svm = SVR()

# Create voting regressor
vr = VotingRegressor(
    estimators=[('lr', lr), ('rf', rf), ('svm', svm)]
)

vr.fit(X_train, y_train)
predictions = vr.predict(X_test)  # Average of individual predictions
```

**Voting Regression Process:**
```
Model 1 Prediction: 100
Model 2 Prediction: 105
Model 3 Prediction: 95
Average: (100 + 105 + 95) / 3 = 100
```

## Weighted Voting

```python
# Give more weight to better-performing models
vc = VotingClassifier(
    estimators=[('lr', lr), ('rf', rf), ('svm', svm)],
    weights=[0.5, 1.0, 0.8],  # RF twice as important
    voting='soft'
)

# Predictions weighted by model importance
```

## Model Selection for Voting

### Diversity Requirements

**Choose models that:**
- Make different types of errors
- Use different algorithms (not all trees)
- Have similar performance level
- Use different features if possible

**Example combinations:**
```
✓ Good: Logistic + Random Forest + SVM (different approaches)
✓ Good: Linear + Tree + Distance-based
✗ Bad: Random Forest + Extra Trees (too similar)
```

## Advantages and Disadvantages

**Advantages:**
✓ Improves over individual models
✓ Reduces overfitting through averaging
✓ Leverages strengths of different algorithms
✓ Robust to individual model failures
✓ Better than best individual model (usually)
✓ Easy to implement

**Disadvantages:**
✗ Slower prediction time (multiple models)
✗ More complex to maintain/update
✗ Loss of interpretability
✗ No guarantee of improvement
✗ Requires training multiple models
✗ Storage overhead

## Performance Comparison

```python
from sklearn.metrics import accuracy_score

# Individual model scores
lr_score = accuracy_score(y_test, lr.predict(X_test))
rf_score = accuracy_score(y_test, rf.predict(X_test))
svm_score = accuracy_score(y_test, svm.predict(X_test))

# Ensemble score
ensemble_score = accuracy_score(y_test, vc.predict(X_test))

print(f"Logistic: {lr_score:.3f}")
print(f"Random Forest: {rf_score:.3f}")
print(f"SVM: {svm_score:.3f}")
print(f"Voting Ensemble: {ensemble_score:.3f}")
```

## Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV

# Tune individual classifiers within voting ensemble
param_grid = {
    'lr__C': [0.1, 1, 10],
    'rf__n_estimators': [50, 100, 200],
    'svm__C': [0.1, 1, 10]
}

grid_search = GridSearchCV(vc, param_grid, cv=5)
grid_search.fit(X_train, y_train)
best_vc = grid_search.best_estimator_
```

## When to Use Voting Ensembles

**Use When:**
- Combination of models improves performance
- Interpretability loss acceptable
- Computational resources sufficient
- Individual models have different strengths
- Need robust predictions

**Don't Use When:**
- Single model sufficient
- Real-time prediction required (latency critical)
- Simple interpretable model needed
- Storage limited
- Individual models highly correlated

## Stacking vs Voting

| Aspect | Voting | Stacking |
|--------|--------|----------|
| Meta-learner | Fixed (average/vote) | Learned model |
| Complexity | Simple | Complex |
| Performance | Good | Better |
| Training | Single round | Multi-round |
| Interpretability | Poor | Very poor |
| Computation | Fast | Slower |

## Best Practices

- Select diverse base learners
- Use models with similar performance levels
- Scale features appropriately
- Use cross-validation for evaluation
- Monitor both individual and ensemble performance
- Consider soft voting for probabilistic output
- Validate on independent test set
- Document model combination rationale
- Compare against individual best models
- Consider computational cost

## Example Workflow

```python
1. Train individual models separately
2. Check performance of each
3. Create voting ensemble
4. Evaluate ensemble on test set
5. Compare with individual models
6. Use ensemble if performance improves
7. Fine-tune ensemble parameters
8. Deploy ensemble model
```

## Key Learnings

✓ Ensemble methods leverage multiple perspectives
✓ Voting provides simple but effective combination
✓ Diversity among base learners crucial
✓ Often outperforms individual models
✓ Trade-off between performance and complexity
✓ Soft voting usually better than hard voting
✓ Building block for more advanced ensembles
✓ Production-proven technique
