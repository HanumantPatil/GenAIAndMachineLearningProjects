---
title: PracticeCode
description: Python and machine learning practice repository with scripts, notebooks, and sample datasets for statistics and regression exercises, credit risk analysis, and shared study notes.
---

## Overview

PracticeCode is a comprehensive hands-on learning repository for Python, NumPy, pandas, statistics, and machine learning fundamentals. It includes standalone scripts, Jupyter notebooks, CSV datasets, and complete ML projects used across topics like distributions, confidence intervals, regression, classification, clustering, ensemble methods, feature engineering, model evaluation, credit risk analysis, and shared study notes.

## Repository Structure

### Core Python & Data Libraries
* `num.py`, `number.py`, `numpy_examples.py`, `pandas01.py`: Core Python and data library practice scripts
* `bill_survey.csv`, `heights.csv`, `miles.csv`, `shoe_sales.csv`: Root-level datasets
* Root notebooks: Statistics and probability practice (central limit theorem, confidence scores, confidence intervals, height analysis)

### Regression Models
* `GradientDescent/`: Gradient descent optimization algorithm with implementations and home price dataset
* `PolynomialRegression/`: Non-linear regression using polynomial features

### Classification Models
* `LogsticRegression/`: Binary and multi-class logistic regression with probability calibration
* `decision_tree_model/`: Decision tree implementation with feature importance and visualization
* `RandomForestClassifierModel/`: Ensemble random forest for robust classification
* `SVM_Algo_Model_Classification/`: Support Vector Machines with kernel methods
* `XGBoost_Classifier_Model/`: XGBoost for binary and multi-class classification

### Ensemble & Boosting Methods
* `Gradient_Boosting_Classification/`: Titanic survival prediction with gradient boosting
* `XGBoostingModel/`: Extreme gradient boosting (XGBoost) implementation
* `VotingRrgrassionAndClassifier/`: Voting ensemble combining multiple diverse models

### Unsupervised Learning (Clustering)
* `unsupervised_learning_k_means_model/`: K-Means clustering with elbow method and silhouette analysis
* `DBSCAN_model/`: Density-based clustering for arbitrary cluster shapes
* `Hierarchical_Clustering/`: Agglomerative hierarchical clustering with dendrograms
* `hierarchical_clustering_model/`: Comparison of K-Means vs Hierarchical clustering

### Feature Engineering & Selection
* `OneHotEncoding/`: Categorical variable encoding for ML algorithms
* `feature_selection/`: Feature selection using correlation analysis and redundancy removal
* `VIF_feature_selection/`: Variance Inflation Factor for multicollinearity detection
* `L1_L2_Regularization/`: Lasso and Ridge regularization for overfitting prevention
* `HandleClassImblalance/`: SMOTE, class weights, and threshold optimization for imbalanced data

### Model Optimization & Evaluation
* `hyper_parameter_tuning_grid_search_cv/`: Exhaustive hyperparameter search using Grid Search
* `HyperParameterTuning_randomized_search_cv/`: Efficient random hyperparameter search
* `K_Fold_Validation/`: K-Fold cross-validation for robust model evaluation
* `stratified_k_fold_cross_validation/`: Stratified K-Fold for maintaining class distribution
* `Model_Evaluation/`: Comprehensive evaluation metrics and validation strategies
* `ModelEvalution/`: Train/test split tutorials and evaluation techniques
* `model_selection_guide/`: Decision guide for choosing appropriate algorithms

### Specialized Projects
* `health_insurance_cost_prediector/`: Complete ML application with Streamlit UI for insurance cost prediction
  - Includes data cleaning, feature engineering, model training, and web application
* `ATM_Card_ML_Model/`: Financial fraud detection/risk assessment project
* `cradit_risk_prediector/`: Credit risk default prediction project with feature engineering, Optuna experiments, and rank-order/KS evaluation

### Reference Notes
* `Notes/`: Curated PDF takeaways for supervised learning, feature engineering, model evaluation, and the ML project lifecycle

### Infrastructure & Design
* `ML_Ops/`: Machine Learning Operations - deployment, monitoring, versioning, retraining pipelines
* `LLD/`: Low-Level Design (LLD) - Object-Oriented Programming principles and design patterns

## Learning Paths

### Beginner: Fundamentals
1. Start with root-level scripts: `num.py`, `numpy_examples.py`, `pandas01.py`
2. Review statistics notebooks: `central_limit_theorm.ipynb`, `confidence_interval.ipynb`
3. Explore basic regression: `GradientDescent/`, `PolynomialRegression/`
4. Learn preprocessing: `OneHotEncoding/`, `feature_selection/`

### Intermediate: Core Algorithms
1. Classification: `LogsticRegression/` → `decision_tree_model/` → `RandomForestClassifierModel/`
2. Regression: `House_Prediector_Model/` → `Gradient_Boosting_Model/`
3. Clustering: `unsupervised_learning_k_means_model/` → `Hierarchical_Clustering/` → `DBSCAN_model/`
4. Feature Engineering: `VIF_feature_selection/` → `L1_L2_Regularization/` → `HandleClassImblalance/`

### Advanced: Optimization & Ensemble
1. Hyperparameter Tuning: `hyper_parameter_tuning_grid_search_cv/` → `HyperParameterTuning_randomized_search_cv/`
2. Ensemble Methods: `Gradient_Boosting_Classification/` → `XGBoostingModel/` → `VotingRrgrassionAndClassifier/`
3. Validation: `K_Fold_Validation/` → `stratified_k_fold_cross_validation/`
4. Evaluation: `Model_Evaluation/` → `model_selection_guide/`

### Expert: Real-World Projects
1. Complete ML Application: `health_insurance_cost_prediector/` (Streamlit + ML)
2. Financial ML: `ATM_Card_ML_Model/` (Fraud Detection)
3. Credit Risk Modeling: `cradit_risk_prediector/` (default prediction, feature engineering, KS evaluation)
4. Operations: `ML_Ops/` (Production ML)
5. Design: `LLD/` (Software Architecture)
6. Study Notes: `Notes/` (topic takeaways and review PDFs)

## Key Features

✅ **36 level-1 project folders** documented across the workspace
✅ **Comprehensive Documentation** covering theory and implementation
✅ **Algorithm Comparisons** to understand trade-offs
✅ **Best Practices** for production-ready code
✅ **Real-World Projects** with Streamlit applications
✅ **Complete Examples** from data cleaning to deployment
✅ **Mathematical Foundations** with equations and explanations
✅ **Evaluation Metrics** guides for all problem types
✅ **Cross-Validation** strategies for robust modeling

## Updated Solutions

* Added folder-level documentation for the credit risk project and the shared notes index so the top-level navigation covers every level-1 folder.
* Added an updated income bucket analysis in `health_insurance_cost_prediector/data_cleaning/ml_premium_prediction_imp.ipynb` using `pd.cut` and `pd.crosstab`.
* The income ranges are grouped as `<10L`, `10L-25L`, `25L-40L`, and `>40L` before generating the contingency table.
* The notebook now visualizes this grouped crosstab with a stacked bar chart and uses the same `crosstab` output for the heatmap.
* The repository now keeps folder-level README coverage aligned with the documented level-1 project structure.

## Prerequisites

* Python 3.10 or later
* `pip`

## Environment Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## How to Run

### Python Scripts
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run Python scripts
python number.py
python numpy_examples.py
python pandas01.py
```

### Jupyter Notebooks
Open notebooks from the workspace in VS Code and run cells using the selected Python kernel from `.venv`.

### Streamlit Applications
```powershell
# Health Insurance Cost Predictor
.\.venv\Scripts\Activate.ps1
streamlit run health_insurance_cost_prediector/app/main.py
```

### Explore Specific Topics
Each folder contains a dedicated `README.md` file with:
- Theory and key concepts
- Implementation details
- Example code and workflows
- Best practices
- Learning outcomes
- Performance metrics

Browse to any folder and open its README for detailed guidance.

### Example: Running Decision Trees
```powershell
# Navigate to decision tree folder
cd decision_tree_model

# Open the README for complete information
# Read decision_tree_model/README.md

# Run the notebook
jupyter notebook 9_decision_tree_salary_classification.ipynb
```

## Quick Navigation by Topic

### Looking for...

**Classification?**
- Logistic Regression → `LogsticRegression/`
- Decision Trees → `decision_tree_model/`
- Random Forest → `RandomForestClassifierModel/`
- SVM → `SVM_Algo_Model_Classification/`
- XGBoost → `XGBoost_Classifier_Model/`
- Multi-class → `MultiClassClassificationModel/`
- Text Classification → `Spam_Classification/`

**Regression?**
- Linear Regression → `GradientDescent/`, `House_Prediector_Model/`
- Polynomial Regression → `PolynomialRegression/`
- Gradient Boosting → `Gradient_Boosting_Model/`
- XGBoost → `XGBoostingModel/`

**Clustering?**
- K-Means → `unsupervised_learning_k_means_model/`
- Hierarchical → `Hierarchical_Clustering/`
- DBSCAN → `DBSCAN_model/`
- Comparison → `hierarchical_clustering_model/`

**Feature Engineering?**
- Encoding → `OneHotEncoding/`
- Feature Selection → `feature_selection/`
- Multicollinearity → `VIF_feature_selection/`
- Regularization → `L1_L2_Regularization/`
- Class Imbalance → `HandleClassImblalance/`

**Model Optimization?**
- Hyperparameter Tuning → `hyper_parameter_tuning_grid_search_cv/`, `HyperParameterTuning_randomized_search_cv/`
- Cross-Validation → `K_Fold_Validation/`, `stratified_k_fold_cross_validation/`
- Evaluation → `Model_Evaluation/`, `ModelEvalution/`
- Algorithm Selection → `model_selection_guide/`

**Ensemble Methods?**
- Gradient Boosting → `Gradient_Boosting_Classification/`, `Gradient_Boosting_Model/`
- XGBoost → `XGBoostingModel/`, `XGBoost_Classifier_Model/`
- Voting Ensemble → `VotingRrgrassionAndClassifier/`

**Production & Design?**
- Complete ML App → `health_insurance_cost_prediector/`
- Financial ML → `ATM_Card_ML_Model/`
- MLOps → `ML_Ops/`
- Software Design → `LLD/`

## Documentation

Every folder contains a comprehensive `README.md` with:
- **Overview**: Topic description and relevance
- **Key Concepts**: Theory and mathematical foundations
- **Prerequisites**: Required libraries and knowledge
- **Key Learning Outcomes**: What you'll master
- **Implementation**: Code examples and workflows
- **Algorithms & Formulas**: Mathematical details
- **Best Practices**: Production-ready guidelines
- **Performance Metrics**: Evaluation and comparison
- **Real-World Applications**: Practical use cases
- **Common Mistakes**: Pitfalls to avoid
- **Key Learnings**: Summary of insights

## Notes

* Every level-1 project folder now includes a detailed `README.md` for quick reference and comprehensive learning
* Folder names are kept as-is to preserve existing notebook paths and references
* Some topic folders contain similarly named datasets for isolated practice scenarios
* Root-level README provides complete navigation and learning path guidance
* Each folder's README is self-contained and can be read independently or as part of the structured learning path
* All level-1 project folders are documented with theory, implementation, and best practices
* Use the Learning Paths section to follow a structured progression from beginner to expert level
