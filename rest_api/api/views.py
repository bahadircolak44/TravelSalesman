import json
import traceback

from api.serializers import LocationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.pub_sub import PubSub
from utils.logger import APP_LOGGER


class LocationView(APIView):
    def post(self, *args, **kwargs):
        """
        endpoints allowing the customer to input problem instances
        and obtain results from the underlying pub/sub queues.

        Example:
        [POST] /api/v1/problems/
         - request
            {
                "max_travel_distance": 3000,
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
                    [104, 113], [104, 121], [104, 129], [104, 137], [104, 145]
                ]
            }
         - response
            {
                "0": {
                    "route": [0, 4, 6, 7, 9, 10, 11, 13, 14, 15, 16, 20, 21, 22, 23, 43, 44, 45, 46, 2, 1, 0],
                    "cost": 537
                },
                "1": {
                    "route": [0, 3, 42, 39, 29, 30, 31, 32, 34, 35, 33, 36, 40, 0],
                    "cost": 630
                },
                "2": {
                    "route": [0, 41, 38, 37, 24, 28, 27, 26, 25, 19, 18, 17, 12, 8, 5, 0],
                    "cost": 627
                }
            }
        """
        try:
            serializer = LocationSerializer(data=self.request.data)
            if serializer.is_valid():
                APP_LOGGER.info(serializer.validated_data)
                solution = PubSub().emit(json.dumps(serializer.validated_data))
                return Response(solution, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            APP_LOGGER.error(traceback.format_exc())