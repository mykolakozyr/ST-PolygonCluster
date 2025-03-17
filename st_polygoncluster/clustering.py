import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.sparse.csgraph import connected_components
from scipy.sparse import csr_matrix
from st_polygoncluster.neighbors import find_overlapping_neighbors

def cluster_polygons(gdf: gpd.GeoDataFrame, time_key: str = None, time_threshold: int = 3600) -> gpd.GeoDataFrame:
    """
    Clusters polygons using DBSCAN or HDBSCAN based on spatial intersection and temporal proximity.
    Adds a `cluster_id` column to the GeoDataFrame.
    
    Parameters:
    - gdf: GeoDataFrame with polygon geometries
    - time_key: Optional column for temporal clustering
    - time_threshold: Time difference (in seconds) to consider polygons in the same cluster
    
    Returns:
    - GeoDataFrame with `cluster_id`
    """
    neighbors = find_overlapping_neighbors(gdf)
    
    # Convert neighbor dictionary to adjacency matrix
    adjacency_matrix = np.zeros((len(gdf), len(gdf)))
    for idx, neighbors_list in neighbors.items():
        for neighbor in neighbors_list:
            adjacency_matrix[idx, neighbor] = 1
            adjacency_matrix[neighbor, idx] = 1  # Symmetric matrix
    
    if time_key:
        times = gdf[time_key].apply(lambda x: x.timestamp()).values # Convert to UNIX timestamps
        time_diff_matrix = np.abs(np.subtract.outer(times, times))  # Correct multi-dimensional indexing
        
        # Only filter time on existing spatial neighbors (preserve 0s)
        adjacency_matrix = np.where((time_diff_matrix > time_threshold) & (adjacency_matrix == 1), 0, adjacency_matrix)
    
    # Convert adjacency matrix to a sparse graph format
    graph = csr_matrix(adjacency_matrix)

    # Find connected components (clusters)
    n_components, labels = connected_components(csgraph=graph, directed=False)

    # Assign cluster IDs
    gdf["cluster_id"] = labels
    return gdf