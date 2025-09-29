# ST-PolygonCluster

## Overview
This library provides tools for clustering polygon geometries based on spatial and temporal proximity. Unlike traditional clustering libraries that focus on point geometries, this library is designed to handle polygons, identifying neighbors through overlapping geometries.

This library is provided as-is, mainly as a reference implementation. It may not receive frequent updates, but feel free to open issues or forks.

## Use case
The motivation for this tool originated from a satellite tasking order analysis use case. Many commercial satellite data providers offer a tasking-based data collection service, where customers submit orders for specific areas of interest—typically defined as polygons. The satellite (or constellation) then collects data over these areas, often capturing imagery in overlapping strips.

This analysis aims to reconstruct the original ordered area based on captured satellite images. The approach clusters spatially overlapping satellite captures while considering a temporal threshold (e.g., 10 days - see example below) to group images that likely correspond to the same tasking request.

<img width="816" alt="st-polygoncluster" src="https://github.com/user-attachments/assets/73d72b6d-6f88-4b5c-a54f-9ff31ea17040" />

## Features
- **Polygon-Based Clustering**: Works with polygon geometries instead of just points.
- **Neighbor Detection**: Uses true polygon intersection with a configurable overlap threshold.
- **Optional Temporal Component**: Clusters can incorporate a time-based proximity metric.
- **Minimum Cluster Size**: Optionally enforce a minimum number of polygons per cluster, labeling smaller components as noise.
- **Designed for GeoDataFrames**: Works directly with `geopandas.GeoDataFrame` objects.
- **Efficient Spatial Indexing**: Uses an R-tree index for fast neighbor lookup.
- **Transitive Closure**: Ensures that indirectly connected polygons belong to the same cluster.
- **Sparse Adjacency Representation**: Improves scalability for large datasets.

## Installation
The library is not currently published at PyPi. One of the ways of using it - get it directly from GitHub.

```bash
pip install git+https://github.com/mykolakozyr/ST-PolygonCluster.git
```

## Usage
```python
import geopandas as gpd
from st_polygoncluster.clustering import cluster_polygons

# Load a sample dataset
gdf = gpd.read_file("./data/example.geojson")

# Run clustering (raise overlap_threshold if you need stricter overlap; defaults to 0%)
clustered_gdf = cluster_polygons(
    gdf,
    time_key="timestamp",
    time_threshold=600,
    min_cluster_size=2,
    overlap_threshold=50,
)

# Save results
clustered_gdf.to_file("./data/clustered_output.geojson", driver="GeoJSON")
```

## Parameters
- **gdf**: GeoDataFrame with polygon geometries
- **time_key**: Optional column name for temporal clustering (e.g., "timestamp")
- **time_threshold**: Time difference in seconds to consider polygons in the same cluster (default: 3600)
- **min_cluster_size**: Minimum number of polygons required to form a valid cluster. Components smaller than this are assigned `cluster_id = -1`.
- **overlap_threshold**: Minimum intersection-over-union percentage (0-100) required for polygons to be considered neighbors (default: 0).

## TODO
- Add alternate overlap metrics (e.g., symmetric coverage) alongside IoU.

## How It Works
1. **Find Neighbors:** Polygons are evaluated based on **true intersection** (not just BBOX).
2. **Apply Time Constraints (if enabled):** Polygons are only clustered together if they fall within the specified **time threshold**.
3. **Ensure Transitive Closure:** If polygon A overlaps with B and B overlaps with C, **all three will be in the same cluster**.
4. **Assign Cluster IDs:** Connected components are extracted using an adjacency graph and labeled accordingly.
