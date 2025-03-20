# ST-PolygonCluster

## Overview
This library provides tools for clustering polygon geometries based on spatial and temporal proximity. Unlike traditional clustering libraries that focus on point geometries, this library is designed to handle polygons, identifying neighbors through overlapping geometries.

## Use case

The idea for the tool came from a specific use case connected with satellite tasking ordering analytics. Most commercial satellite data providers have a "tasking" type of data collection. Their customers place orders for specific areas (often defined as a polygon), and then the satellite (constellation) data collection for this area. Satellites capture data in strips that overlap.

The idea of the analysis is to derive the original order area based on satellite captures.

## Features
- **Polygon-Based Clustering**: Works with polygon geometries instead of just points.
- **Neighbor Detection**: Uses true polygon intersection.
- **Optional Temporal Component**: Clusters can incorporate a time-based proximity metric.
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
clustered_gdf = cluster_polygons(gdf, time_key="timestamp", time_threshold=600)

# Save results
clustered_gdf.to_file("./data/clustered_output.geojson", driver="GeoJSON")

# Print results
print(clustered_gdf[["geometry", "cluster_id"]])
```

## TODO
- Be able to define the **number of elements per cluster**.
- Define the **overlap % threshold** for neighbor detection.

## How It Works
1. **Find Neighbors:** Polygons are evaluated based on **true intersection** (not just BBOX).
2. **Apply Time Constraints (if enabled):** Polygons are only clustered together if they fall within the specified **time threshold**.
3. **Ensure Transitive Closure:** If polygon A overlaps with B and B overlaps with C, **all three will be in the same cluster**.
4. **Assign Cluster IDs:** Connected components are extracted using an adjacency graph and labeled accordingly.

## Contributions
PRs are welcome! If you find a bug or want to add a feature, feel free to submit an issue or open a pull request.
