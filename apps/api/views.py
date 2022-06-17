import django_filters.rest_framework
from api.serializers import DataPointSerializer, PlantSerializer
from plants.models import DataPoint, Plant
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class PlantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plant.objects.all().prefetch_related("plant_data", "data_types__plant_data")
    serializer_class = PlantSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()

        return super().get_queryset().filter(user=self.request.user)

    @action(detail=True, methods=["get"])
    def charts(self, request, pk=None):
        """
        This endpoint will return an objects chart data.

        Each chart object will have various properties, including its time series, data series, and various metadata.
        This can be used to populate charts outside of the main website!
        """

        return Response(self.get_object().to_chart_data())


class PlantDataViewSet(viewsets.ModelViewSet):
    queryset = DataPoint.objects.all()
    serializer_class = DataPointSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()

        return super().get_queryset().filter(plant__user=self.request.user)
