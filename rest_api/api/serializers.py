from rest_framework import serializers


class NoModelSerializer(serializers.Serializer):
    """
    """

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class CoordinatePairSerializer(NoModelSerializer):
    coordinates = serializers.ListSerializer(child=serializers.ListSerializer(child=serializers.FloatField()))
