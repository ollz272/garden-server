import abc

from api.v1.serializers import DataPointSerializer, PlantSerializer, SensorSerializer
from plants.models import DataPoint, Plant, Sensor
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.throttling import UserRateThrottle


class PlantBelongsToUserMixin:
    @abc.abstractmethod
    def get_plant(self, serializer: Serializer) -> Plant:
        """
        Function to grab the plant
        """


class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all().prefetch_related("sensors", "sensors__plant_data")
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    throttle_classes = [UserRateThrottle]
    serializer_class = PlantSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()

        return super().get_queryset().filter(user=self.request.user)

    @action(detail=True, methods=["get"])
    def charts(self, request, pk=None):
        """
        This endpoint will return an objects chart data.

        Each chart object will have various properties, including its time series, data series, and various metadata.
        This can be used to populate charts outside the main website!
        """

        return Response(self.get_object().to_chart_data())

    @action(detail=True, methods=["post"])
    def create_sensor(self, request, pk=None):
        """
        Endpoint to create a data type for a plant
        """

        return Response({})

    @action(detail=True, methods=["get"])
    def get_sensors(self, request, pk=None):
        """
        Endpoint to create a data type for a plant
        """

        return Response(SensorSerializer(Sensor.objects.filter(plant_id=pk), many=True).data)

    @action(detail=True, methods=["post"])
    def create_data(self, request, pk=None):
        """
        Endpoint to create data for a plants data type
        """

        return Response({})

    @action(detail=True, methods=["get"])
    def get_timeseries_data(self, request, pk=None):
        """
        Endpoint to get the time series data for a plant
        """
        resp = {
            data_type.id: [DataPointSerializer(dp).data for dp in data_type.plant_data.all()]
            for data_type in Sensor.objects.filter(plant_id=pk).prefetch_related("plant_data")
        }
        return Response(resp)


class SensorViewSet(PlantBelongsToUserMixin, viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    serializer_class = SensorSerializer

    def get_plant(self, serializer: SensorSerializer) -> Plant:
        plant = serializer.data["plant"]
        return Plant.objects.get(id=plant)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()

        return super().get_queryset().filter(plant__user=self.request.user)


class PlantDataViewSet(PlantBelongsToUserMixin, viewsets.ModelViewSet):
    queryset = DataPoint.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    serializer_class = DataPointSerializer

    def get_plant(self, serializer: SensorSerializer) -> Plant:
        plant = serializer.data["plant"]
        return Plant.objects.get(id=plant)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()

        return super().get_queryset().filter(plant__user=self.request.user)
