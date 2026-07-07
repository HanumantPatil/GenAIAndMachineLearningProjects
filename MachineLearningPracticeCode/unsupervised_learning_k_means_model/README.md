# K-Means Clustering - Unsupervised Learning

## Overview

This folder contains implementations of **K-Means Clustering**, a fundamental unsupervised learning algorithm that partitions data into k clusters by iteratively assigning points to nearest centroids.

## Key Concepts

- **Clustering**: Grouping similar data points without labels
- **Centroids**: Cluster centers (mean of points in cluster)
- **Within-Cluster Variance**: Minimization objective
- **Euclidean Distance**: Distance metric for assignment
- **Convergence**: Iterative refinement until stability
- **Elbow Method**: Determining optimal cluster count

## Prerequisites

```
numpy
pandas
matplotlib
seaborn
scikit-learn
scipy
```

## Key Learning Outcomes

✓ K-Means algorithm and intuition
✓ Initialization strategies (random, k-means++)
✓ Determining optimal number of clusters (k)
✓ Convergence criteria and iterations
✓ Feature scaling and preprocessing
✓ Cluster quality metrics (inertia, silhouette score)
✓ Handling outliers and noise
✓ Prediction on new data
✓ Comparison with other clustering methods
✓ Real-world applications

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run notebooks or scripts in this folder
jupyter notebook *.ipynb
python *.py
```

## K-Means Algorithm Steps

1. **Initialize**: Select k initial centroids randomly or using k-means++
2. **Assign**: Assign each point to nearest centroid
3. **Update**: Calculate new centroids as mean of assigned points
4. **Iterate**: Repeat steps 2-3 until convergence
5. **Converge**: When centroids stop changing (or max iterations)

## Determining Optimal k

**Elbow Method:**
```
Plot inertia vs k
Look for "elbow" point where improvement plateaus
```

**Silhouette Score:**
```
Range [-1, 1]
Score > 0.5 indicates good cluster separation
```

**Gap Statistic:**
```
Compares clustering to random uniform distribution
```

## K-Means Variants

| Variant | Characteristics |
|---------|-----------------|
| Standard | Basic implementation |
| k-means++ | Better initialization (avoids poor local minima) |
| Mini-batch | For large datasets (memory efficient) |
| Spherical | For normalized data on unit sphere |

## Mathematical Foundation

**Objective Function (Minimize):**
```
J = Σ Σ ||xᵢ - μⱼ||²
```

**Centroid Update:**
```
μⱼ = (1/nⱼ) * Σ xᵢ (for all xᵢ in cluster j)
```

## Silhouette Score Interpretation

```
s(i) = (b(i) - a(i)) / max(a(i), b(i))

Where:
a(i) = average distance to other points in same cluster
b(i) = average distance to points in nearest cluster

Range: [-1, 1]
> 0.5: Good separation
0 to 0.5: Moderate separation
< 0: Poor separation
```

## Advantages and Disadvantages

**Advantages:**
✓ Simple and fast algorithm
✓ Scales well to large datasets
✓ Easy to implement and understand
✓ Versatile across domains

**Disadvantages:**
✗ Requires specifying k in advance
✗ Sensitive to initialization
✗ Assumes spherical clusters
✗ May converge to local minimum
✗ Fails with non-convex cluster shapes

## Best Practices

- Try k-means++ for better initialization
- Scale features to same range before clustering
- Use Elbow method + Silhouette score together
- Try multiple random initializations
- Validate clusters make business sense
- Use mini-batch for large datasets
- Document cluster interpretation
- Monitor convergence iterations
- Consider alternative methods for non-convex data

## Preprocessing Steps

1. Load data and explore
2. Handle missing values
3. Remove outliers (if appropriate)
4. Feature scaling/normalization
5. Feature selection/reduction
6. Apply K-Means
7. Evaluate and interpret

## Key Learnings

✓ K-Means intuitive clustering algorithm
✓ Foundation for many advanced techniques
✓ Widely used in practice
✓ Determining k crucial for success
✓ Proper initialization and scaling essential
✓ Complemented by evaluation metrics
✓ Building block for more complex methods (GMM, etc.)
