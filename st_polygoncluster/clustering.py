import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.sparse.csgraph import connected_components
from scipy.sparse import csr_matrix
from st_polygoncluster.neighbors import find_overlapping_neighbors

def cluster_polygons(
    gdf: gpd.GeoDataFrame,
    time_key: str = None,
    time_threshold: int = 3600,
    min_cluster_size: int = 1,
    overlap_threshold: float = 0.0,
) -> gpd.GeoDataFrame:
    """
    Clusters polygons based on spatial intersection and temporal proximity.
    Ensures transitive closure only within actual connected components.
    
    Parameters:
    - gdf: GeoDataFrame with polygon geometries
    - time_key: Optional column for temporal clustering
    - time_threshold: Time difference (in seconds) to consider polygons in the same cluster
    - min_cluster_size: Minimum number of elements required for a cluster to be valid.
      Clusters smaller than this threshold are labeled as -1.
    - overlap_threshold: Minimum intersection-over-union percentage (0-100) required
      for polygons to be considered neighbors. Defaults to 0.
    
    Returns:
    - GeoDataFrame with `cluster_id`
    """
    neighbors = find_overlapping_neighbors(gdf, overlap_threshold=overlap_threshold)

    # Build adjacency matrix
    adjacency_matrix = np.zeros((len(gdf), len(gdf)))
    for idx, neighbors_list in neighbors.items():
        for neighbor in neighbors_list:
            adjacency_matrix[idx, neighbor] = 1
            adjacency_matrix[neighbor, idx] = 1  # Symmetric matrix

    if time_key:
        times = gdf[time_key].apply(lambda x: x.timestamp()).values  # Convert to UNIX timestamps
        time_diff_matrix = np.abs(np.subtract.outer(times, times))
        adjacency_matrix[time_diff_matrix > time_threshold] = 0  # Remove time-inconsistent neighbors

    # Convert adjacency matrix to a sparse graph
    graph = csr_matrix(adjacency_matrix)

    # Compute connected components **without over-expanding clusters**
    n_components, labels = connected_components(csgraph=graph, directed=False)

    # Enforce minimum cluster size: mark clusters smaller than threshold as noise (-1)
    if min_cluster_size is not None and min_cluster_size > 1:
        # Count elements per component label
        label_counts = pd.Series(labels).value_counts()
        small_labels = set(label_counts[label_counts < min_cluster_size].index.tolist())
        if small_labels:
            labels = np.array([-1 if lbl in small_labels else int(lbl) for lbl in labels])

    gdf["cluster_id"] = labels
    return gdf
