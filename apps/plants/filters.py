import django_filters
from plants.forms import PlantDataFilterForm
from plants.models import Plant


class PlantDataFilter(django_filters.FilterSet):
    time = django_filters.DateTimeFromToRangeFilter(
        field_name="time",
        widget=django_filters.widgets.RangeWidget(attrs={"type": "datetime-local"}),
    )
    resolution = django_filters.ChoiceFilter()

    class Meta:
        model = Plant
        form = PlantDataFilterForm
        fields = ["time"]

    @property
    def qs(self):
        return super().qs.order_by("time")
