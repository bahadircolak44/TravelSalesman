from rest_framework import serializers


class NoModelSerializer(serializers.Serializer):
    """
    Serializer without model.
    """

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class LocationSerializer(NoModelSerializer):
    locations = serializers.ListSerializer(child=serializers.ListSerializer(child=serializers.FloatField()))
    num_vehicles = serializers.IntegerField()
    depot = serializers.IntegerField()
    max_travel_distance = serializers.IntegerField()
