import django_filters.rest_framework
from api.serializers import DataPointSerializer, PlantSerializer
from plants.models import DataPoint, Plant
from rest_framework import viewsets


class PlantViewSet(viewsets.ModelViewSet):
    """ """

    queryset = Plant.objects.all().prefetch_related("plant_data")
    serializer_class = PlantSerializer


class PlantDataViewSet(viewsets.ModelViewSet):
    queryset = DataPoint.objects.all()
    serializer_class = DataPointSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["plant", "time"]
