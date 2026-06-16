# Health Insurance Cost Predictor

## Overview

This folder contains a **complete machine learning project** for predicting health insurance costs using customer demographics, health indicators, and lifestyle factors. The project includes data cleaning, model development, and a Streamlit web application for interactive predictions.

## Contents

- `app/`: Streamlit web application for predictions
  - `main.py`: Streamlit UI and input interface
  - `prediection_helper.py`: Model prediction logic
- `data_cleaning/`: Data preprocessing and exploration
- `SOW/`: Statement of Work and project documentation

## Key Concepts

- **Feature Engineering**: Creating meaningful predictive features
- **Data Preprocessing**: Cleaning and transforming raw data
- **Categorical Encoding**: Converting categorical variables to numerical
- **Feature Selection**: Identifying important predictors
- **Model Training**: Building predictive models
- **Hyperparameter Tuning**: Optimizing model performance
- **Web Application**: User-friendly prediction interface

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
streamlit
```

## How to Run

### Data Cleaning & Model Development
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run Jupyter notebooks in data_cleaning folder
jupyter notebook data_cleaning/
```

### Streamlit Web Application
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run the Streamlit app
streamlit run app/main.py
```

The application will open at `http://localhost:8501`

## Input Features

### Demographic Information
- **Age**: Customer age (18-100 years)
- **Number of Dependants**: Number of family members covered
- **Gender**: Male/Female

### Financial Information
- **Income**: Annual income in Lakhs (Indian currency)
- **Employment Status**: Salaried/Self-Employed/Freelancer

### Health & Lifestyle
- **BMI Category**: Body Mass Index classification
- **Smoking Status**: Non-smoker/Occasional/Regular
- **Medical History**: Pre-existing conditions

### Insurance Selection
- **Insurance Plan**: Bronze/Silver/Gold
- **Region**: Geographic location (Northwest/Southeast/Northeast/Southwest)
- **Genetical Risk**: Family history risk factor (0-5 scale)

## Features Explanation

| Feature | Impact | Description |
|---------|--------|-------------|
| Age | High | Older age typically higher costs |
| Smoking Status | Very High | Smoking significantly increases costs |
| Medical History | Very High | Pre-existing conditions affect costs |
| BMI Category | High | Obesity-related conditions increase costs |
| Income | Medium | May indicate lifestyle/health choices |
| Insurance Plan | High | Premium tier directly affects cost |
| Region | Medium | Geographic variation in healthcare costs |
| Employment | Low | May correlate with benefits/health coverage |

## Project Structure

```
health_insurance_cost_prediector/
├── README.md
├── app/
│   ├── main.py                    # Streamlit web UI
│   └── prediection_helper.py     # Prediction logic
├── data_cleaning/
│   ├── notebooks with analysis/
│   ├── ml_premium_prediction.ipynb
│   └── data files
└── SOW/
    └── Project documentation
```

## Model Development Workflow

1. **Data Exploration**: Analyze feature distributions and correlations
2. **Data Cleaning**: Handle missing values, outliers, inconsistencies
3. **Feature Engineering**: Create new features, encode categorical variables
4. **Feature Selection**: Remove redundant features using correlation/VIF
5. **Model Selection**: Try multiple algorithms (Linear, Tree-based, Ensemble)
6. **Hyperparameter Tuning**: Optimize model parameters
7. **Cross-Validation**: Validate with K-Fold CV
8. **Evaluation**: Assess performance with regression metrics
9. **Deployment**: Integrate into Streamlit app

## Expected Model Performance

Models typically achieve:
- **R² Score**: 0.70-0.85 (explains 70-85% of variance)
- **RMSE**: Varies by scale, typically within 10-20% of mean prediction
- **MAE**: Average prediction error

## Categorical Variables Encoding

```python
categorical_options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Unmarried', 'Married'],
    'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'Smoking Status': ['No Smoking', 'Regular', 'Occasional'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer'],
    'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold'],
    'Medical History': ['No Disease', 'Diabetes', 'High blood pressure', ...]
}
```

## Best Practices Applied

✓ **Data Validation**: Input validation in Streamlit app
✓ **Feature Scaling**: Normalized features for model consistency
✓ **Cross-Validation**: Robust model evaluation
✓ **Hyperparameter Tuning**: Grid/Random search optimization
✓ **Error Handling**: Graceful handling of edge cases
✓ **Documentation**: Clear code comments and docstrings
✓ **User Interface**: Intuitive Streamlit layout
✓ **Prediction Interpretation**: Clear output and confidence

## Model Interpretation

Feature importances show which factors most influence predictions:
1. **Smoking Status**: Typically most important
2. **Medical History**: Pre-existing conditions matter
3. **Age**: Increases with age
4. **Insurance Plan**: Premium tier affects cost
5. **BMI Category**: Health indicator

## Business Insights

- Young, healthy non-smokers pay less
- Smokers pay significantly more
- Pre-existing conditions increase costs substantially
- Gold plans cost more than Bronze plans
- Regional variation exists in healthcare costs

## Performance Metrics

Typical metrics for regression:
- **MAE** (Mean Absolute Error): Average prediction error
- **RMSE** (Root Mean Squared Error): Penalizes large errors
- **R² Score**: Proportion of variance explained
- **Cross-validation Score**: Average performance across folds

## Future Enhancements

- Include real-world claim history
- Add temporal trends (inflation, market changes)
- Ensemble multiple model predictions
- Geographic cost index refinement
- Integration with insurance backend
- Model retraining pipeline
- A/B testing for prediction improvements

## Key Learnings

✓ End-to-end ML project from data to deployment
✓ Real-world data cleaning challenges
✓ Feature engineering for healthcare domain
✓ Categorical encoding strategies
✓ Model selection and comparison
✓ Web application development with Streamlit
✓ User-friendly prediction interface
✓ Business problem to technical solution
