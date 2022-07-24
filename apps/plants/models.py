from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse
from django.utils.text import slugify
from colorfield.fields import ColorField


class Plant(models.Model):
    """
    Model representing our plant which we want to track data from.
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    indoor = models.BooleanField()
    slug = models.SlugField()

    class Meta:
        constraints = [UniqueConstraint(fields=["user", "name"], name="unique_plant_name_for_user")]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)

    def to_chart_data(self):
        charts = {}
        for data_type in self.data_types.all():
            data_points = self.plant_data.filter(data_type=data_type)
            charts[data_type.slug] = {
                "time": [data.time for data in data_points],
                "data": [data.data for data in data_points],
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
            UniqueConstraint(fields=("plant", "colour"), name="unique_chart_colour",)
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
    time = models.DateTimeField(auto_now_add=True)
    data_type = models.ForeignKey(DataType, on_delete=models.CASCADE, related_name="plant_data")
    data = models.FloatField()

    class Meta:
        ordering = ("-time",)

    def __str__(self):
        return f"Data point for {self.plant} at {self.time}"
