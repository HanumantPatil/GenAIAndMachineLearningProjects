# DBSCAN Model - Density-Based Clustering

## Overview

This folder contains implementations of **DBSCAN (Density-Based Spatial Clustering of Applications with Noise)**, a powerful unsupervised learning algorithm for clustering data based on density rather than distance or distribution.

## Contents

- `dbscan_synthetic_data.ipynb`: DBSCAN applied to synthetic datasets
- `dbscan_synthetic_data_imp.ipynb`: Improved implementation with optimizations
- `dbscan_customer_segmentation.ipynb`: Customer segmentation using DBSCAN
- `dbscan_customer_segmentation_imp.ipynb`: Enhanced customer segmentation implementation
- `income.xlsx`: Sample income dataset for clustering

## Key Concepts

- **DBSCAN Algorithm**: Density-based clustering that discovers clusters of arbitrary shapes
- **Epsilon (eps)**: Distance threshold for neighbors
- **Min Points**: Minimum points required to form a dense region
- **Core Points, Border Points, Noise Points**: Classification of data points
- **Noise Handling**: Automatic identification of outliers as noise points

## Files & Notebooks

### `dbscan_synthetic_data.ipynb`
- Basic DBSCAN implementation on synthetic datasets
- Parameter tuning (eps, min_samples)
- Visualization of clusters and noise points
- Comparison with K-means clustering

### `dbscan_synthetic_data_imp.ipynb`
- Optimized DBSCAN implementation
- Advanced parameter selection techniques
- Performance metrics and evaluation
- Cluster quality assessment

### `dbscan_customer_segmentation.ipynb`
- Real-world application on customer income data
- Data preprocessing and standardization
- Customer segmentation into clusters
- Business insights from clustering

### `dbscan_customer_segmentation_imp.ipynb`
- Enhanced customer segmentation
- Advanced metrics (silhouette score, davies-bouldin index)
- Visualization of customer segments
- Actionable insights for business

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
scipy
```

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run Jupyter notebook
jupyter notebook dbscan_synthetic_data.ipynb
```

## Key Learnings

✓ When to use DBSCAN vs K-means
✓ How to select optimal eps and min_samples
✓ Handling noise and outliers in clustering
✓ Customer segmentation for business analytics
✓ Visualization and interpretation of clusters
