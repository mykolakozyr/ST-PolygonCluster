# ST-PolygonCluster

## Overview
This library provides tools for clustering polygon geometries based on spatial and temporal proximity. Unlike traditional clustering libraries that focus on point geometries, this library is designed to handle polygons, identifying neighbors through overlapping geometries.

## Features
- **Polygon-Based Clustering**: Works with polygon geometries instead of just points.
- **Neighbor Detection**:
  - Uses true polygon intersection.
- **Optional Temporal Component**: Clusters can incorporate a time-based proximity metric.
- **Designed for GeoDataFrames**: Works directly with `geopandas.GeoDataFrame` objects.
- **Efficient Spatial Indexing**: Uses an R-tree index for fast neighbor lookup.
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
clustered_gdf = cluster_polygons(gdf, time_key="timestamp", time_threshold=600)

# Save results
clustered_gdf.to_file("./data/clustered_output.geojson", driver="GeoJSON")

# Print results
print(clustered_gdf[["geometry", "cluster_id"]])
```

## TODO
- Be able to define the **number of elements per cluster**.
- Define the **overlap % threshold** for neighbor detection.
