# Gradient Descent - Optimization Algorithm

## Overview

This folder contains implementations of **Gradient Descent**, a fundamental optimization algorithm used in machine learning to minimize loss functions and train models.

## Contents

- `gradient_descent.py`: Basic Gradient Descent implementation
- `gradient_descent_imp.py`: Improved implementation with variants
- `home_prices.csv`: Housing dataset for regression

## Key Concepts

- **Gradient Descent**: Iterative optimization algorithm
- **Learning Rate**: Step size controlling convergence speed
- **Loss Function**: Measuring prediction error
- **Convergence**: Reaching minimum of loss function
- **Local vs Global Minima**: Optimization challenges
- **Batch, Stochastic, Mini-batch GD**: Different variants

## Files & Scripts

### `gradient_descent.py`
- Basic Gradient Descent implementation from scratch
- Step-by-step explanation of the algorithm
- Visualization of convergence
- Application to linear regression

### `gradient_descent_imp.py`
- Improved implementations with multiple variants:
  - Batch Gradient Descent
  - Stochastic Gradient Descent (SGD)
  - Mini-batch Gradient Descent
- Momentum and acceleration techniques
- Adaptive learning rates
- Performance comparison

## Dataset

**home_prices.csv**: Housing dataset
- Features: Square footage, location, etc.
- Target: House prices
- Used for: Regression and optimization demonstration

## Prerequisites

```
numpy
pandas
matplotlib
scikit-learn
```

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run Python script
python gradient_descent.py
python gradient_descent_imp.py
```

## Gradient Descent Variants

✓ **Batch GD**: Uses entire dataset for each update
✓ **Stochastic GD (SGD)**: Uses single sample for each update
✓ **Mini-batch GD**: Uses subset of data for each update
✓ **Momentum**: Accelerates convergence
✓ **Nesterov Accelerated Gradient (NAG)**
✓ **Adam**: Adaptive learning rate method

## Key Learnings

✓ How Gradient Descent minimizes loss functions
✓ Impact of learning rate on convergence
✓ Comparison of different GD variants
✓ Numerical stability considerations
✓ Feature scaling importance
✓ Convergence criteria and stopping conditions
