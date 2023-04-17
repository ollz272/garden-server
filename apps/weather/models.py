from django.contrib.gis.db import models as gis_models
from django.db import models

# Create your models here.


class Weather(models.Model):
    """
    A weather point.

    Based on data from https://open-meteo.com/
    """

    # Meta Data
    date_time = models.DateTimeField()
    location = gis_models.PointField()

    # Data about weather
    temperature = models.FloatField()
    apparent_temperature = models.FloatField()
    rain = models.FloatField()
    cloud_cover = models.FloatField()
    weather_code = models.FloatField()  # TODO there are choices.

    class Meta:
        constraints = [
            models.UniqueConstraint(name="unique_weather_for_location_time", fields=["date_time", "location"])
        ]
