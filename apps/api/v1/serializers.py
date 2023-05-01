from plants.models import DataPoint, Plant, Sensor
from rest_framework import serializers


class DataPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPoint
        fields = ["plant", "time", "sensor", "data"]

    def validate(self, data):
        """
        Check the sensor belongs to the plant.
        """
        if data["sensor"] not in data["plant"].sensors.all():
            raise serializers.ValidationError(f"Data type does not belong to plant '{data['plant']}'.")

        return data


class PlantDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPoint
        fields = [
            "time",
            "data",
        ]


class SensorSerializer(serializers.ModelSerializer):
    plant_data = PlantDataSerializer(many=True, read_only=True)

    class Meta:
        model = Sensor
        fields = ["id", "name", "slug", "unit", "colour", "plant", "plant_data"]


class PlantSerializer(serializers.ModelSerializer):
    sensors = SensorSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Plant
        fields = ["id", "user", "name", "sensors"]
        read_only_fields = ("user",)
        depth = 1
