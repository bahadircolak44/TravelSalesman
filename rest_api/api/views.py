import json

from api.serializers import CoordinatePairSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.pub_sub import PubSub


class CoordinatePairView(APIView):
    def get(self, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        serializer = CoordinatePairSerializer(data=self.request.data)
        if serializer.is_valid():
            # print(serializer.validated_data.get('coordinates'))
            solution = PubSub().emit(json.dumps(serializer.validated_data.get('coordinates')))
            return Response(solution, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
