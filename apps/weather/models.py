from django.contrib.gis.db import models as gis_models
from django.db import models

from weather import choices

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
    weather_code = models.FloatField(choices=choices.WeatherTypes.choices)

    is_forecast = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(name="unique_weather_for_location_time", fields=["date_time", "location"])
        ]
        indexes = [
            models.Index(fields=["date_time"]),
            models.Index(fields=["location"]),
            models.Index(fields=["is_forecast"]),
            models.Index(fields=["weather_code"]),
        ]

    def __str__(self):
        return f"Weather at {self.location} on {self.date_time}"
