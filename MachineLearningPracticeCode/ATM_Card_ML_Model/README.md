# ATM Card Machine Learning Model

## Overview

This folder contains a **machine learning project for ATM card fraud detection or risk assessment**, demonstrating real-world classification challenges in the financial services domain.

## Contents

- `SOW/`: Statement of Work and project documentation

## Key Concepts

- **Fraud Detection**: Identifying suspicious transactions
- **Financial Data Analysis**: Working with banking data
- **Risk Assessment**: Predicting card-related risks
- **Class Imbalance**: Fraud typically rare in transaction data
- **Feature Engineering**: Creating features from transaction patterns
- **Model Interpretability**: Explaining fraud decisions to stakeholders

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
```

## Key Learning Outcomes

✓ Real-world classification problem in finance
✓ Handling imbalanced fraud/non-fraud data
✓ Feature engineering for transaction data
✓ Interpretability requirements for fraud detection
✓ Cross-validation for robust evaluation
✓ Business metrics (false positive/false negative costs)
✓ Model deployment considerations
✓ Regulatory and compliance requirements

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run notebooks or scripts in this folder
jupyter notebook *.ipynb
python *.py
```

## Project Phases

### Phase 1: Data Understanding
- Load ATM/card transaction data
- Explore fraud vs non-fraud patterns
- Identify key features
- Analyze class distribution

### Phase 2: Data Preparation
- Handle missing values
- Feature engineering from transaction data
- Feature scaling for algorithms
- Address class imbalance (SMOTE, weights)

### Phase 3: Model Development
- Select appropriate algorithms
- Train multiple models
- Hyperparameter tuning
- Cross-validation evaluation

### Phase 4: Model Evaluation
- Precision/Recall trade-offs
- ROC-AUC analysis
- Confusion matrix review
- Business impact assessment

### Phase 5: Deployment
- Model serialization
- Integration with banking systems
- Monitoring and retraining

## Common Challenges

- **Class Imbalance**: Fraud is ~0.1-1% of transactions
- **Real-time Latency**: Must make decisions quickly
- **Feature Limitations**: Limited data in real-time
- **Concept Drift**: Fraud patterns change over time
- **False Positives**: Blocking legitimate transactions hurts customers
- **False Negatives**: Missing frauds costs money
- **Regulatory**: Compliance and audit requirements

## Typical Features Used

**Transaction Features:**
- Amount
- Timestamp
- Merchant category
- Location
- Frequency of transactions

**Cardholder Features:**
- Account age
- Historical spending patterns
- Account type
- Geographic region

**Behavioral Features:**
- Deviation from normal pattern
- Unusual merchant category
- Unusual amount
- Unusual time

## Evaluation Metrics

| Metric | Importance | Trade-off |
|--------|-----------|----------|
| **Precision** | High | False alarms block customers |
| **Recall** | High | Missing fraud costs money |
| **Specificity** | High | Must approve legitimate transactions |
| **F1-Score** | Medium | Balance metric |
| **ROC-AUC** | Medium | Threshold independent |

## Business Considerations

**Costs of Errors:**
- FP (False Positive): Customer frustration, call center cost
- FN (False Negative): Financial loss from fraud

**Threshold Adjustment:**
- Can adjust decision threshold based on costs
- Higher threshold → more precision, less recall
- Lower threshold → more recall, less precision

## Model Interpretability

**Why Important:**
- Customers want to know why card was blocked
- Regulators require explainability
- Compliance audits need documentation
- Trust and transparency critical

**Interpretability Techniques:**
- Feature importance scores
- SHAP values for individual predictions
- Model-agnostic explanation methods
- Rule-based decision explanations

## Real-World Deployment

```
1. Model Development (offline)
2. Model Testing & Validation
3. Staging Environment (similar to prod)
4. Canary Deployment (small % traffic)
5. Full Production Deployment
6. Monitoring & Logging
7. Periodic Retraining
8. Performance Tracking
```

## Monitoring in Production

**Key Metrics:**
- Model accuracy on recent data
- Fraud detection rate
- False positive rate
- System latency
- Model drift detection

## Regulatory Considerations

- **GDPR**: Data privacy and consent
- **PCI-DSS**: Payment card security
- **Fair Lending**: Non-discriminatory decisions
- **Audit Trail**: Explainability requirements

## Best Practices

- Document all decisions and rationale
- Maintain model version control
- Monitor for data/concept drift
- Regular retraining cycles
- A/B testing for model improvements
- Stakeholder communication
- Compliance documentation
- Test for fairness and bias

## Further Reading

- Model Explainability (SHAP, LIME)
- Concept Drift Detection
- Online Learning for Fraud Detection
- Ensemble Methods for Fraud Detection
- Cost-Sensitive Learning

## Key Learnings

✓ Real-world ML addresses business problems
✓ Class imbalance common in fraud detection
✓ Interpretability crucial in finance
✓ Business metrics differ from ML metrics
✓ Model monitoring essential post-deployment
✓ Regulatory compliance non-negotiable
✓ Continuous improvement necessary
✓ Domain expertise + ML = effective solution
