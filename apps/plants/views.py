from django.shortcuts import render
from plants.filters import PlantDataFilter
from plants.models import DataPoint


def plants(request):
    f = PlantDataFilter(request.GET, queryset=DataPoint.objects.all().select_related("plant"))
    data_sets = {}
    for plant in f.qs.values_list("plant", flat=True).distinct():
        data_sets[plant] = f.qs.filter(plant=plant)
    return render(request, "plants/chart_new.html", {"filter": f, "data_sets": data_sets})
