import django_filters
from plants.models import DataPoint, Plant


class PlantDataFilter(django_filters.FilterSet):
    plant = django_filters.ModelMultipleChoiceFilter(
        queryset=Plant.objects.all(), to_field_name="id", conjoined=True, method="filter_plants"
    )

    time = django_filters.DateTimeFromToRangeFilter(field_name="time")

    class Meta:
        model = DataPoint
        fields = ["plant", "time"]

    @property
    def qs(self):

        return super().qs.order_by("time")

    def filter_plants(self, queryset, name, value):
        return queryset.filter(plant__in=value)
