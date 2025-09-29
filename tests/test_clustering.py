import geopandas as gpd
import unittest
from shapely.geometry import Polygon

from st_polygoncluster.clustering import cluster_polygons

class TestClustering(unittest.TestCase):
    def setUp(self):
        # Load the example dataset
        self.gdf = gpd.read_file("./data/example.geojson")

    def test_cluster_polygons_small_time(self):
        """Test clustering with a strict temporal threshold where the third polygon is separate."""
        clustered_gdf = cluster_polygons(self.gdf, time_key="timestamp", time_threshold=600, overlap_threshold=10)  # 10 min
        cluster_labels = clustered_gdf["cluster_id"].tolist()
        
        # Expecting two clusters: first two polygons in one, third separate, fourth separate
        self.assertEqual(cluster_labels[0], cluster_labels[1])  # First two should be in the same cluster
        self.assertNotEqual(cluster_labels[0], cluster_labels[2])  # Third should be separate
        self.assertNotEqual(cluster_labels[0], cluster_labels[3])  # Fourth should be separate

    def test_cluster_polygons_large_time(self):
        """Test clustering with a relaxed temporal threshold where the third polygon joins the cluster."""
        clustered_gdf = cluster_polygons(self.gdf, time_key="timestamp", time_threshold=7200, overlap_threshold=10)  # 2 hours
        cluster_labels = clustered_gdf["cluster_id"].tolist()
        
        # Expecting one main cluster (first three polygons) and one separate (fourth polygon)
        self.assertEqual(cluster_labels[0], cluster_labels[1])  # First two should be in the same cluster
        self.assertEqual(cluster_labels[0], cluster_labels[2])  # Third should also be in the same cluster
        self.assertNotEqual(cluster_labels[0], cluster_labels[3])  # Fourth should be separate

    def test_min_cluster_size(self):
        """Clusters smaller than min_cluster_size should be labeled as -1 (noise)."""
        clustered_gdf = cluster_polygons(self.gdf, time_key="timestamp", time_threshold=7200, min_cluster_size=3, overlap_threshold=10)
        cluster_labels = clustered_gdf["cluster_id"].tolist()

        # With relaxed time, first three polygons form a cluster of size 3; fourth is alone and should be -1
        self.assertEqual(cluster_labels[0], cluster_labels[1])
        self.assertEqual(cluster_labels[0], cluster_labels[2])
        self.assertEqual(cluster_labels[3], -1)

    def test_overlap_threshold_controls_cluster_membership(self):
        square_a = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
        square_b = Polygon([(0.2, 0.2), (1.2, 0.2), (1.2, 1.2), (0.2, 1.2)])
        gdf = gpd.GeoDataFrame({"geometry": [square_a, square_b]}, geometry="geometry", crs="EPSG:4326")

        strict_clusters = cluster_polygons(gdf.copy(), overlap_threshold=50)
        relaxed_clusters = cluster_polygons(gdf.copy(), overlap_threshold=40)

        strict_labels = strict_clusters["cluster_id"].tolist()
        relaxed_labels = relaxed_clusters["cluster_id"].tolist()

        self.assertNotEqual(strict_labels[0], strict_labels[1])
        self.assertEqual(relaxed_labels[0], relaxed_labels[1])

if __name__ == "__main__":
    unittest.main()
