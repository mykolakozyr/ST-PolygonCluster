import geopandas as gpd
import unittest
from shapely.geometry import Polygon

from st_polygoncluster.neighbors import find_overlapping_neighbors

class TestNeighbors(unittest.TestCase):
    def setUp(self):
        # Load the example dataset
        self.gdf = gpd.read_file("./data/example.geojson")

    def test_find_overlapping_neighbors(self):
        neighbors = find_overlapping_neighbors(self.gdf, overlap_threshold=10)

        # First three polygons should have overlapping neighbors
        self.assertTrue(1 in neighbors[0])
        self.assertTrue(2 in neighbors[0])
        self.assertTrue(0 in neighbors[1])
        self.assertTrue(2 in neighbors[1])
        self.assertTrue(0 in neighbors[2])
        self.assertTrue(1 in neighbors[2])
        
        # The fourth polygon (far away) should have no neighbors
        self.assertEqual(neighbors[3], [])

    def test_overlap_threshold_filters_neighbors(self):
        square_a = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
        square_b = Polygon([(0.2, 0.2), (1.2, 0.2), (1.2, 1.2), (0.2, 1.2)])
        gdf = gpd.GeoDataFrame({"geometry": [square_a, square_b]}, geometry="geometry", crs="EPSG:4326")

        relaxed_neighbors = find_overlapping_neighbors(gdf, overlap_threshold=40)
        strict_neighbors = find_overlapping_neighbors(gdf, overlap_threshold=50)

        self.assertTrue(1 in relaxed_neighbors[0])
        self.assertEqual(relaxed_neighbors[1], [0])
        self.assertEqual(strict_neighbors, {0: [], 1: []})

if __name__ == "__main__":
    unittest.main()
