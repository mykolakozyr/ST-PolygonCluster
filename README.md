# ST-PolygonCluster

## Overview
This library provides tools for clustering polygon geometries based on spatial and temporal proximity. Unlike traditional clustering libraries that focus on point geometries, this library is designed to handle polygons, identifying neighbors through overlapping geometries.

## Use case
The motivation for this tool originated from a satellite tasking order analysis use case. Many commercial satellite data providers offer a tasking-based data collection service, where customers submit orders for specific areas of interest—typically defined as polygons. The satellite (or constellation) then collects data over these areas, often capturing imagery in overlapping strips.

This analysis aims to reconstruct the original ordered area based on captured satellite images. The approach clusters spatially overlapping satellite captures while considering a temporal threshold (e.g., 10 days - see example below) to group images that likely correspond to the same tasking request.

<img width="816" alt="st-polygoncluster" src="https://github.com/user-attachments/assets/73d72b6d-6f88-4b5c-a54f-9ff31ea17040" />

## Features
- **Polygon-Based Clustering**: Works with polygon geometries instead of just points.
- **Neighbor Detection**: Uses true polygon intersection.
- **Optional Temporal Component**: Clusters can incorporate a time-based proximity metric.
- **Minimum Cluster Size**: Optionally enforce a minimum number of polygons per cluster, labeling smaller components as noise.
- **Designed for GeoDataFrames**: Works directly with `geopandas.GeoDataFrame` objects.
- **Efficient Spatial Indexing**: Uses an R-tree index for fast neighbor lookup.
- **Transitive Closure**: Ensures that indirectly connected polygons belong to the same cluster.
- **Sparse Adjacency Representation**: Improves scalability for large datasets.

## Installation
```bash
pip install st-polygoncluster
```

## Usage
```python
import geopandas as gpd
from st_polygoncluster.clustering import cluster_polygons

# Load a sample dataset
gdf = gpd.read_file("./data/example.geojson")

# Run clustering
clustered_gdf = cluster_polygons(gdf, time_key="timestamp", time_threshold=600, min_cluster_size=2)

# Save results
clustered_gdf.to_file("./data/clustered_output.geojson", driver="GeoJSON")
```

## Parameters
- **min_cluster_size**: Minimum number of polygons required to form a valid cluster. Components smaller than this are assigned `cluster_id = -1`.

## TODO
- Define the **overlap % threshold** for neighbor detection.

## How It Works
1. **Find Neighbors:** Polygons are evaluated based on **true intersection** (not just BBOX).
2. **Apply Time Constraints (if enabled):** Polygons are only clustered together if they fall within the specified **time threshold**.
3. **Ensure Transitive Closure:** If polygon A overlaps with B and B overlaps with C, **all three will be in the same cluster**.
4. **Assign Cluster IDs:** Connected components are extracted using an adjacency graph and labeled accordingly.

## Contributions
PRs are welcome! If you find a bug or want to add a feature, feel free to submit an issue or open a pull request.
