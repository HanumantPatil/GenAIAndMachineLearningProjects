# Spam Classification

## Overview

This folder contains implementations of **spam email classification**, a practical text classification problem using machine learning to distinguish spam from legitimate emails.

## Key Concepts

- **Text Classification**: Categorizing text documents
- **Feature Extraction**: Converting text to numerical features
- **TF-IDF**: Term Frequency-Inverse Document Frequency
- **Bag of Words**: Simple text representation
- **Naive Bayes**: Probabilistic classification
- **Feature Engineering**: Relevant feature creation for text

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
nltk
```

## Key Learning Outcomes

✓ Text preprocessing (tokenization, stemming, lemmatization)
✓ Feature extraction from text (TF-IDF, Bag of Words)
✓ Naive Bayes for text classification
✓ Performance metrics for imbalanced classification
✓ Cross-validation for text data
✓ Confusion matrix interpretation
✓ ROC-AUC for spam classification
✓ Model deployment considerations
✓ Real-world text classification challenges

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run notebooks or scripts in this folder
jupyter notebook *.ipynb
python *.py
```

## Text Preprocessing Pipeline

1. **Lowercase**: Convert to lowercase
2. **Remove Punctuation**: Strip special characters
3. **Tokenization**: Split into words
4. **Remove Stopwords**: Filter common words (the, a, is, etc.)
5. **Stemming/Lemmatization**: Reduce words to base form
6. **Feature Extraction**: Convert to numerical features

## Feature Extraction Methods

### Bag of Words
```
Document: "spam email is bad"
Vector: [spam:1, email:1, is:1, bad:1]
```

### TF-IDF
```
TF-IDF = Term Frequency × Inverse Document Frequency
Highlights important, document-specific words
```

### N-grams
```
Unigrams: "spam", "email"
Bigrams: "spam email", "email is"
Captures word sequences
```

## Naive Bayes for Text

**Probability Formula:**
```
P(Spam|words) = P(words|Spam) × P(Spam) / P(words)
```

**Advantages for Text:**
✓ Fast and efficient
✓ Works well with text features
✓ Probabilistic output
✓ Scalable to large datasets

## Handling Imbalanced Data (Few Spams)

| Technique | Description |
|-----------|-------------|
| SMOTE | Generate synthetic spam samples |
| Class Weights | Penalize spam misclassification more |
| Threshold Adjustment | Lower threshold for spam detection |
| Stratified K-Fold | Maintain class distribution in folds |

## Performance Metrics for Spam

| Metric | Importance | Why |
|--------|-----------|-----|
| Precision | High | Minimize false positives (blocking legit emails) |
| Recall | High | Minimize false negatives (missing spams) |
| F1-Score | Both | Balance precision and recall |
| Specificity | Medium | Catching legitimate emails |

## Confusion Matrix for Spam

```
                Predicted
            Spam    | Not Spam
Actual  S | TP      | FN (missed spams)
        N | FP (false alerts) | TN

Key Focus:
- Minimize FP: Don't block legitimate emails
- Minimize FN: Don't miss spams
```

## Real-World Considerations

- **Spam Evolution**: Models need regular retraining
- **Class Imbalance**: Spam typically <5% of emails
- **Multi-language**: Support different languages
- **Encoding Detection**: Handle various email formats
- **Feature Explosion**: Too many unique words
- **Domain Adaptation**: Different patterns by domain
- **Interpretability**: Why marked as spam?

## Best Practices

- Preprocess text consistently (train & test)
- Use TF-IDF for better features than raw counts
- Remove rare/common words appropriately
- Handle misspellings and variations
- Use stratified cross-validation
- Monitor false positive rate closely
- Combine multiple classification models (ensemble)
- Validate on real data, not just metrics
- Update models regularly with new spam patterns

## Pipeline Example

```python
1. Load email data
2. Preprocess text (lowercase, tokenize, remove stopwords)
3. Extract TF-IDF features
4. Split train/test with stratification
5. Train Naive Bayes classifier
6. Evaluate: precision, recall, F1, AUC-ROC
7. Adjust threshold if needed
8. Deploy and monitor
```

## Key Learnings

✓ Text classification fundamental NLP task
✓ Preprocessing crucial for text data
✓ TF-IDF effective feature extraction
✓ Naive Bayes strong baseline for text
✓ Imbalanced classification challenges
✓ Precision important for user experience
✓ Real-world spam constantly evolving
✓ Ensemble methods often improve performance
