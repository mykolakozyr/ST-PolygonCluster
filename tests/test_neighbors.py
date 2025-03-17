import geopandas as gpd
import unittest
from st_polygoncluster.neighbors import find_overlapping_neighbors

class TestNeighbors(unittest.TestCase):
    def setUp(self):
        # Load the example dataset
        self.gdf = gpd.read_file("./data/example.geojson")

    def test_find_overlapping_neighbors(self):
        neighbors = find_overlapping_neighbors(self.gdf)
        print("Neighbors Dictionary:", neighbors)

        
        # First three polygons should have overlapping neighbors
        self.assertTrue(1 in neighbors[0])
        self.assertTrue(2 in neighbors[0])
        self.assertTrue(0 in neighbors[1])
        self.assertTrue(2 in neighbors[1])
        self.assertTrue(0 in neighbors[2])
        self.assertTrue(1 in neighbors[2])
        
        # The fourth polygon (far away) should have no neighbors
        self.assertEqual(neighbors[3], [])

if __name__ == "__main__":
    unittest.main()