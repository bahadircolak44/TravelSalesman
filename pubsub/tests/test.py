import unittest
from ortool import compute_euclidean_distance_matrix
from tests import initial_data


class TestPubSubMethods(unittest.TestCase):
    def test_euclidean_distance_matrix(self):
        result = compute_euclidean_distance_matrix(initial_data.locations)
        self.assertEqual(initial_data.distance_matrix, result)
