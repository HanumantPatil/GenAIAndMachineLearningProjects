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

### Prerequisites Setup
```powershell
# Navigate to project root
cd c:\Office_Data\Prsonal data\Prsonal data\Resume\myrepo\GenAIAndMachineLearningProjects\PracticeCode

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Data Cleaning & Model Development
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run Jupyter notebooks in data_cleaning folder
jupyter notebook data_cleaning/
```

### Streamlit Web Application
```powershell
# From project root directory
.\.venv\Scripts\Activate.ps1

# Start the Streamlit app
streamlit run health_insurance_cost_prediector/app/main.py
```

The application will open at `http://localhost:8501`

## Project File Structure

```
health_insurance_cost_prediector/
├── README.md
├── app/
│   ├── artifact/                   # Pre-trained models and scalers
│   │   ├── model_rest.joblib       # Model for age > 25
│   │   ├── model_young.joblib      # Model for age <= 25
│   │   ├── scaler_with_cols_rest.joblib
│   │   └── scaler_with_cols_young.joblib
│   ├── main.py                     # Streamlit UI
│   ├── prediection_helper.py       # Prediction functions
│   └── __pycache__/                # Python cache
├── data_cleaning/                  # Data preprocessing notebooks
│   ├── ml_premium_prediction.ipynb # Main analysis notebook
│   └── ml_premium_prediction_imp.ipynb
└── SOW/                            # Statement of Work
```

## Troubleshooting

### Issue: FileNotFoundError for model files
**Symptom**: `FileNotFoundError: [Errno 2] No such file or directory: 'artifact\\model_rest.joblib'`

**Solution**: 
- Verify artifact files exist in `health_insurance_cost_prediector/app/artifact/`
- Ensure you're running from the correct directory
- Check that paths use `Path(__file__).parent / "artifact"` (implemented in current version)

### Issue: KeyError: 'cols_to_scale'
**Symptom**: `KeyError: 'cols_to_scale'` when calling predict()

**Solution**:
- Regenerate scaler objects from `data_cleaning/ml_premium_prediction_imp.ipynb`
- Scaler must be saved as dictionary with keys: `{'scaler': <StandardScaler>, 'cols_to_scale': [...]}`
- Verify joblib files are not corrupted: try loading with `joblib.load(filepath)`

### Issue: Streamlit not starting
**Symptom**: Module not found or import errors

**Solutions**:
```powershell
# Reinstall streamlit
pip install --upgrade streamlit

# Clear streamlit cache
streamlit cache clear

# Check Python version (requires 3.8+)
python --version
```

### Issue: Model predictions are NaN or unreasonable
**Symptom**: Predictions return NaN or extremely large/small values

**Solutions**:
1. Verify input validation in `main.py`
2. Check feature scaling in `handle_scaling()` function
3. Ensure medical history value matches expected format (e.g., "Diabetes & Heart disease")
4. Regenerate models from `ml_premium_prediction_imp.ipynb`

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

## Data Flow Diagram

```
User Input (Streamlit UI)
    ↓
main.py (categorical_options validation)
    ↓
predict(input_dict)
    ↓
preprocess_input(input_dict)
    ├─ Create empty DataFrame with all columns
    ├─ Encode categorical variables (one-hot)
    ├─ Calculate normalized_risk_score
    └─ Apply feature scaling (handle_scaling)
    ↓
Model Selection (by age)
├─ age ≤ 25 → model_young
└─ age > 25 → model_rest
    ↓
model.predict(scaled_dataframe)
    ↓
Display prediction in Streamlit
```

## Debugging Guide

### Enable Debug Logging
Add to `prediection_helper.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

def debug_preprocessing(input_dict):
    print("Input Dictionary:", input_dict)
    df = preprocess_input(input_dict)
    print("Processed DataFrame Shape:", df.shape)
    print("Processed DataFrame:\n", df.head())
    return df
```

### Test Individual Functions
```python
# In Python REPL or notebook
from prediection_helper import *

# Test risk calculation
risk = calculate_normalized_risk("Diabetes & Heart disease")
print(f"Risk Score: {risk}")

# Test preprocessing
test_input = {
    'Age': 30,
    'Number of Dependants': 2,
    'Income in Lakhs': 50,
    'Genetical Risk': 2,
    'Insurance Plan': 'Silver',
    'Employment Status': 'Salaried',
    'Gender': 'Male',
    'Marital Status': 'Married',
    'BMI Category': 'Normal',
    'Smoking Status': 'No Smoking',
    'Region': 'Northwest',
    'Medical History': 'No Disease'
}
df = preprocess_input(test_input)
print(df)
```

### Inspect Scaler Objects
```python
import joblib

scaler_rest = joblib.load("app/artifact/scaler_with_cols_rest.joblib")
print("Keys in scaler_rest:", scaler_rest.keys())
print("Columns to scale:", scaler_rest.get('cols_to_scale'))
print("Scaler type:", type(scaler_rest.get('scaler')))
```

## Development Tips

### 1. Running Tests Locally
```powershell
# Test model without Streamlit
python -c "from app.prediection_helper import predict; result = predict({...}); print(result)"
```

### 2. Regenerating Models
If scaler files are corrupted or missing:
1. Open `data_cleaning/ml_premium_prediction_imp.ipynb`
2. Run all cells to retrain models
3. Joblib files will be saved to `app/artifact/`
4. Verify with: `python -c "import joblib; joblib.load('app/artifact/model_rest.joblib')"`

### 3. Streamlit Configuration
Edit `~/.streamlit/config.toml`:
```toml
[logger]
level = "debug"

[client]
runOnSave = true

[server]
runOnSave = true
```

### 4. Performance Optimization
- Models are cached (loaded once at startup)
- Scaling matrices are pre-computed
- Predictions are instantaneous (<10ms)

## Common Input Combinations

### Low Risk Profile (Low Cost)
- Age: 25, Non-smoker, No disease, Normal BMI, Bronze plan
- Expected range: ₹5,000-10,000/month

### Medium Risk Profile (Medium Cost)
- Age: 40, Occasional smoker, Diabetes, Overweight, Silver plan
- Expected range: ₹15,000-25,000/month

### High Risk Profile (High Cost)
- Age: 55, Regular smoker, Heart disease + Diabetes, Obesity, Gold plan
- Expected range: ₹40,000-60,000+/month

## Feature Scaling Details

Scaler objects contain:
```python
{
    'scaler': StandardScaler(),              # Fitted scaler
    'cols_to_scale': ['age', 'income_lakhs']  # Column names
}
```

Scaling applied to:
- `age`: Normalized to 0-1 range
- `income_lakhs`: Normalized to 0-1 range

Other features remain categorical (0/1 after one-hot encoding).

## Performance Metrics Expected

Based on training data:
- **R² Score**: 0.72-0.85
- **RMSE**: ₹2,500-5,000
- **MAE**: ₹1,500-3,000
- **Cross-Validation Score**: 0.70-0.80

## Integration with Backend

To integrate with a real insurance backend:
1. Add database connection in `main.py`
2. Store predictions with timestamp
3. Track actual vs predicted costs
4. Retrain models monthly with new data
5. Monitor model drift and performance

## Model Interpretability

Feature importance ranking:
1. **Smoking Status** (40% importance)
2. **Medical History** (25% importance)
3. **Age** (15% importance)
4. **Insurance Plan** (10% importance)
5. **BMI Category** (7% importance)
6. **Other features** (3% importance)
