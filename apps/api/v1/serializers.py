from plants.models import DataPoint, DataType, Plant
from rest_framework import serializers


class DataPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPoint
        fields = ["plant", "time", "data_type", "data"]

    def validate(self, data):
        """
        Check the data_type belongs to the plant.
        """
        if data["data_type"] not in data["plant"].data_types.all():
            raise serializers.ValidationError(f"Data type does not belong to plant '{data['plant']}'.")

        return data


class PlantDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPoint
        fields = [
            "time",
            "data",
        ]


class DataTypeSerializer(serializers.ModelSerializer):
    plant_data = PlantDataSerializer(many=True, read_only=True)

    class Meta:
        model = DataType
        fields = ["id", "name", "slug", "unit", "colour", "plant", "plant_data"]


class PlantSerializer(serializers.ModelSerializer):
    data_types = DataTypeSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Plant
        fields = ["id", "user", "name", "indoor", "data_types"]
        read_only_fields = ("user",)
        depth = 1
