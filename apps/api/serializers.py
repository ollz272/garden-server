from plants.models import DataPoint, Plant
from rest_framework import serializers


class DataPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPoint
        fields = ["plant", "time", "temperature", "light_level", "moisture_level"]


class PlantDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPoint
        fields = ["time", "temperature", "light_level", "moisture_level"]


class PlantSerializer(serializers.ModelSerializer):
    plant_data = PlantDataSerializer(many=True, read_only=True)

    class Meta:
        model = Plant
        fields = ["id", "name", "indoor", "plant_data"]
        depth = 1
