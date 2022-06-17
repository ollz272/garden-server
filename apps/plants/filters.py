import django_filters
from django import forms
from plants.forms import PlantDataFilterForm
from plants.models import DataPoint, Plant


class PlantDataFilter(django_filters.FilterSet):
    plant = django_filters.ModelMultipleChoiceFilter(
        queryset=Plant.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        to_field_name="id",
        conjoined=True,
        method="filter_plants",
    )

    time = django_filters.DateTimeFromToRangeFilter(
        field_name="time", widget=django_filters.widgets.RangeWidget(attrs={"type": "datetime-local"})
    )

    class Meta:
        model = DataPoint
        form = PlantDataFilterForm
        fields = ["plant", "time"]

    @property
    def qs(self):
        return super().qs.order_by("time")

    def filter_plants(self, queryset, name, value):
        return queryset.filter(plant__in=value)
