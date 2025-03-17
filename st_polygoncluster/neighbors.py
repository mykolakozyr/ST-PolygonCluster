import geopandas as gpd
from shapely.strtree import STRtree

def find_overlapping_neighbors(gdf: gpd.GeoDataFrame) -> dict:
    """
    Efficiently finds overlapping neighbors using a spatial index (R-tree).
    """
    tree = STRtree(gdf.geometry)
    neighbors = {i: [] for i in range(len(gdf))}

    for i, poly in enumerate(gdf.geometry):
        indices = tree.query(poly)  # Find all polygons that intersect per index
        true_neighbors = [idx for idx in indices if gdf.geometry.iloc[i].intersects(gdf.geometry.iloc[idx])]
        neighbors[i] = [idx for idx in true_neighbors if idx != i]  # Remove self

    return neighbors
