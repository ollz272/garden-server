from django.shortcuts import render
from rest_framework import viewsets
import django_filters.rest_framework

# Create your views here.
from api.serializers import PlantSerializer, DataPointSerializer
from plants.models import Plant, DataPoint


class PlantViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = Plant.objects.all().prefetch_related('plant_data')
    serializer_class = PlantSerializer


class PlantDataViewSet(viewsets.ModelViewSet):
    queryset = DataPoint.objects.all()
    serializer_class = DataPointSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['plant', 'time']
