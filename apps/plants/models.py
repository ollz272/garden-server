from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg, UniqueConstraint
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from timescale.db.models.fields import TimescaleDateTimeField
from timescale.db.models.managers import TimescaleManager


class Plant(models.Model):
    """
    Model representing our plant which we want to track data from.
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    indoor = models.BooleanField()
    slug = models.SlugField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user", "name"], name="unique_plant_name_for_user"),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)

    def to_chart_data(self, time_from=None, time_to=None):
        """
        Returns a usable dictionary representing the object as a chart - with optional start & end dates.
        """
        charts = {}
        for data_type in self.data_types.all():
            data_points = DataPoint.timescale.filter(data_type=data_type, plant=self)
            if time_from:
                data_points = data_points.filter(time__gte=time_from)
            if time_to:
                data_points = data_points.filter(time__lte=time_to)

            data_points = data_points.time_bucket("time", "1 minutes").annotate(avg_data=Avg("data"))

            charts[data_type.slug] = {
                "time": [data["bucket"] for data in data_points],
                "data": [data["avg_data"] for data in data_points],
                "chart_title": f"Chart of {data_type.name}",
                "element_id": f"chart-{data_type.slug}",
                "unit": f"{data_type.unit}",
                "colour": f"{data_type.colour}",
            }

        return charts


class DataType(models.Model):
    """
    The type of data to record.
    """

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="data_types")
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    unit = models.CharField(max_length=50)
    colour = models.CharField(max_length=50)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=("plant", "colour"),
                name="unique_chart_colour",
            )
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)

    @property
    def api_url(self):
        return reverse("datapoint-list")

    @property
    def api_example_data(self):
        return {"plant": self.plant.id, "data_type": self.id, "data": "YOUR DATA HERE - MUST BE A NUMBER!"}


class DataPoint(models.Model):
    """
    A data point for a plant, containing information on its statistics at a given time.
    """

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="plant_data")
    time = TimescaleDateTimeField(default=timezone.now, interval="5 minutes")
    data_type = models.ForeignKey(DataType, on_delete=models.CASCADE, related_name="plant_data")
    data = models.FloatField()

    # Managers
    objects = models.Manager()
    timescale = TimescaleManager()

    class Meta:
        ordering = ("-time",)

    def __str__(self):
        return f"Data point for {self.plant} at {self.time}"
