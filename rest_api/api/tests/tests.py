from rest_framework import status
from rest_framework.test import APITestCase

data = {
    "max_travel_distance": 900,
    "num_vehicles": 3,
    "depot": 0,
    "locations": [
        [288, 149], [288, 129], [270, 133], [256, 141], [256, 157], [246, 157],
        [236, 169], [228, 169], [228, 161], [220, 169], [212, 169], [204, 169],
        [104, 161], [104, 169], [90, 165], [80, 157], [64, 157], [64, 165],
        [56, 169], [56, 161], [56, 153], [56, 145], [56, 137], [56, 129],
        [16, 97], [16, 109], [8, 109], [8, 97], [8, 89], [8, 81],
        [8, 73], [8, 65], [8, 57], [16, 57], [8, 49], [8, 41],
        [56, 81], [48, 83], [56, 89], [56, 97], [104, 97], [104, 105],
        [104, 113], [104, 121], [104, 129], [104, 137], [104, 145], [116, 145],
        [64, 21], [72, 25], [80, 25], [80, 25], [80, 41], [88, 49],
        [228, 85], [228, 93], [236, 93], [236, 101], [228, 101], [228, 109],
        [228, 117], [228, 125], [220, 125], [212, 117], [204, 109], [196, 101],
        [188, 93], [180, 93], [180, 101], [180, 109], [180, 117], [180, 125],
        [196, 145], [204, 145], [212, 145], [220, 145], [228, 145], [236, 145],
        [246, 141], [252, 125], [260, 129], [280, 133]
    ]
}


class EndpointTests(APITestCase):
    def test_register_user(self):
        response = self.client.post('/api/v1/problem/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        solution = {"0": {
            "route": [0, 78, 77, 76, 75, 74, 71, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 37, 38, 39, 41, 67, 66,
                      65, 64, 60, 61, 79, 80, 2, 0], "cost": 656}, "1": {
            "route": [0, 3, 62, 70, 40, 36, 33, 35, 34, 32, 31, 30, 29, 28, 27, 26, 25, 23, 46, 11, 10, 9, 4, 0],
            "cost": 659}, "2": {
            "route": [0, 1, 81, 57, 56, 54, 55, 58, 59, 63, 69, 68, 51, 50, 48, 49, 52, 53, 42, 43, 44, 45, 47, 72, 73,
                      8, 7, 6, 5, 0], "cost": 651}}
        self.assertEqual(response.data, solution)
        return response.data.get('id')
