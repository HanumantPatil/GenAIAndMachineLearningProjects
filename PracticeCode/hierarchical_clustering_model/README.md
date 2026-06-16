# Hierarchical Clustering Model - K-means vs Hierarchical Clustering

## Overview

This folder contains comparative analysis of **Hierarchical Clustering** versus **K-means Clustering** on synthetic datasets to understand when to use each algorithm.

## Contents

- `noisy_circles_kmeans_vs_hc.ipynb`: K-means vs Hierarchical clustering on noisy circles
- `noisy_circles_kmeans_vs_hc_imp.ipynb`: Improved comparison with detailed analysis

## Key Concepts

- **K-means**: Partitioning-based clustering
- **Hierarchical Clustering**: Hierarchical partitioning
- **Algorithm Comparison**: Strengths and weaknesses
- **Cluster Shape**: Impact on algorithm selection
- **Non-convex Clusters**: When K-means struggles
- **Dendrogram vs Centroid**: Different representations

## Files & Notebooks

### `noisy_circles_kmeans_vs_hc.ipynb`
- K-means clustering implementation
- Hierarchical clustering implementation
- Visualization of both approaches
- Performance comparison on synthetic data
- Identifying algorithm weaknesses and strengths

### `noisy_circles_kmeans_vs_hc_imp.ipynb`
- Enhanced comparison with multiple datasets
- Parameter tuning for both algorithms
- Quality metrics comparison (silhouette score, Davies-Bouldin index)
- Visual analysis of clustering results
- Recommendations for algorithm selection

## Datasets

**Synthetic Data: Noisy Circles**
- Non-linearly separable clusters
- Tests algorithm robustness
- Highlights K-means limitations with non-convex shapes

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
jupyter notebook noisy_circles_kmeans_vs_hc.ipynb
```

## Algorithm Comparison

| Aspect | K-means | Hierarchical |
|--------|---------|-------------|
| Speed | Fast | Slower |
| Cluster Shape | Convex | Any shape |
| Number of Clusters | Must specify k | Can choose from dendrogram |
| Deterministic | No (random init) | Yes |
| Interpretability | Centroids | Dendrogram |
| Scalability | Better | Worse |

## Key Learnings

✓ K-means works best for convex, well-separated clusters
✓ Hierarchical clustering handles arbitrary shapes
✓ Non-linear cluster detection and visualization
✓ When each algorithm excels or fails
✓ Hybrid approaches combining both methods
✓ Data characteristics influencing algorithm selection
