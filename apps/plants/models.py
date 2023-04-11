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

    def to_chart_data(self, time_from=None, time_to=None, resolution=None):
        """
        Returns a usable dictionary representing the object as a chart - with optional start & end dates.
        """
        charts = {}
        for sensor in self.sensors.all():
            data_points = DataPoint.timescale.filter(sensor=sensor, plant=self)
            if time_from:
                data_points = data_points.filter(time__gte=time_from)
            if time_to:
                data_points = data_points.filter(time__lte=time_to)

            if resolution:
                data_points = data_points.time_bucket("time", resolution).annotate(avg_data=Avg("data"))
            else:
                data_points = data_points.time_bucket("time", "PT1M").annotate(avg_data=Avg("data"))

            charts[sensor.slug] = {
                "time": [data["bucket"] for data in data_points],
                "data": [data["avg_data"] for data in data_points],
                "chart_title": f"Chart of {sensor.name}",
                "element_id": f"chart-{sensor.slug}",
                "unit": f"{sensor.unit}",
                "colour": f"{sensor.colour}",
                "sensor_id": sensor.id,
                "plant_id": self.id,
            }

        return charts


class SensorUnit(models.Model):
    """A unit a sensor is allowed to take.

    This is an admin controlled model.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Sensor(models.Model):
    """
    The type of data to record.
    """

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="sensors")
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    unit = models.ForeignKey(SensorUnit, on_delete=models.SET_NULL, null=True)
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
        return reverse("v1-plant-sensors-list")

    @property
    def api_example_data(self):
        return {
            "plant": self.plant.id,
            "sensor": self.id,
            "data": "YOUR DATA HERE - MUST BE A NUMBER!",
        }


class DataPoint(models.Model):
    """
    A data point for a plant, containing information on its statistics at a given time.
    """

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="plant_data")
    time = TimescaleDateTimeField(default=timezone.now, interval="5 minutes")
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name="plant_data")
    data = models.FloatField()

    # Managers
    objects = models.Manager()
    timescale = TimescaleManager()

    def __str__(self):
        return f"Data point for {self.plant} at {self.time}"
