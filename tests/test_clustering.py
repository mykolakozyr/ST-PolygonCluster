import geopandas as gpd
import unittest
from st_polygoncluster.clustering import cluster_polygons

class TestClustering(unittest.TestCase):
    def setUp(self):
        # Load the example dataset
        self.gdf = gpd.read_file("./data/example.geojson")

    def test_cluster_polygons_small_time(self):
        """Test clustering with a strict temporal threshold where the third polygon is separate."""
        clustered_gdf = cluster_polygons(self.gdf, time_key="timestamp", time_threshold=600)  # 10 min
        cluster_labels = clustered_gdf["cluster_id"].tolist()
        
        # Expecting two clusters: first two polygons in one, third separate, fourth separate
        self.assertEqual(cluster_labels[0], cluster_labels[1])  # First two should be in the same cluster
        self.assertNotEqual(cluster_labels[0], cluster_labels[2])  # Third should be separate
        self.assertNotEqual(cluster_labels[0], cluster_labels[3])  # Fourth should be separate

    def test_cluster_polygons_large_time(self):
        """Test clustering with a relaxed temporal threshold where the third polygon joins the cluster."""
        clustered_gdf = cluster_polygons(self.gdf, time_key="timestamp", time_threshold=7200)  # 2 hours
        cluster_labels = clustered_gdf["cluster_id"].tolist()
        
        # Expecting one main cluster (first three polygons) and one separate (fourth polygon)
        self.assertEqual(cluster_labels[0], cluster_labels[1])  # First two should be in the same cluster
        self.assertEqual(cluster_labels[0], cluster_labels[2])  # Third should also be in the same cluster
        self.assertNotEqual(cluster_labels[0], cluster_labels[3])  # Fourth should be separate

if __name__ == "__main__":
    unittest.main()
