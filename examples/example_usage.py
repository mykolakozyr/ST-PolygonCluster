import geopandas as gpd
from st_polygoncluster.clustering import cluster_polygons

# Load a sample dataset
gdf = gpd.read_file("./data/example.geojson")

# Run clustering
clustered_gdf = cluster_polygons(
    gdf,
    time_key="timestamp",
    time_threshold=72000,
    min_cluster_size=2,
    overlap_threshold=50,
)

# Save results
clustered_gdf.to_file("./data/example_output.geojson", driver="GeoJSON")
