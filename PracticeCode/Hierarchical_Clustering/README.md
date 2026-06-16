# Hierarchical Clustering

## Overview

This folder contains implementations of **Hierarchical Clustering**, an unsupervised learning algorithm that creates a dendrogram (tree-like hierarchical structure) of clusters.

## Contents

- `income_hierarchical_clustering.ipynb`: Hierarchical clustering on income data
- `income_hierarchical_clustering_imp.ipynb`: Improved implementation with optimization

## Key Concepts

- **Agglomerative Clustering**: Bottom-up approach (merging clusters)
- **Divisive Clustering**: Top-down approach (splitting clusters)
- **Linkage Methods**: Single, Complete, Average, Ward linkage
- **Dendrogram**: Tree visualization of hierarchical structure
- **Distance Metrics**: Euclidean, Manhattan, Cosine distances
- **Cluster Cut**: Determining optimal number of clusters

## Files & Notebooks

### `income_hierarchical_clustering.ipynb`
- Basic hierarchical clustering implementation
- Dendrogram visualization and interpretation
- Different linkage methods comparison
- Cluster assignment from dendrogram

### `income_hierarchical_clustering_imp.ipynb`
- Optimized implementation with parameter tuning
- Linkage method selection strategies
- Cluster quality assessment (silhouette score)
- Performance comparison with K-means
- Business insights from clustering

## Datasets

Income dataset for clustering analysis:
- Features: Income levels and demographics
- Objective: Segment customers/population by income
- Used for: Customer segmentation and analysis

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
jupyter notebook income_hierarchical_clustering.ipynb
```

## Linkage Methods

✓ **Single Linkage**: Minimum distance between clusters
✓ **Complete Linkage**: Maximum distance between clusters
✓ **Average Linkage**: Average distance between all points
✓ **Ward Linkage**: Minimizes within-cluster variance (recommended)

## Key Learnings

✓ Agglomerative vs Divisive clustering
✓ How to interpret dendrograms
✓ Selecting appropriate linkage method
✓ Determining optimal number of clusters
✓ Comparison with K-means clustering
✓ Advantages and disadvantages of hierarchical clustering
✓ When to use hierarchical clustering
