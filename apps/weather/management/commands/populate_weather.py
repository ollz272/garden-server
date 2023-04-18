import requests
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from weather.models import Weather
import datetime as dt


class Command(BaseCommand):
    """Command for populating weather into the database.

    Populated from https://open-meteo.com/
    """

    url = (
        "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&hourly=temperature_2m,apparent_temperature,"
        "rain,weathercode,cloudcover&past_days=7&forecast_days=7"
    )

    def handle(self, *args, **options):
        # TODO get lat/lon from database.
        for lat, lon in [(52.52, 13.41), (52.40, -2.01)]:
            resp = requests.get(self.url.format(lat, lon)).json()
            now = dt.datetime.now()

            for time, temp, apparent_temp, rain, weather_code, cloud_cover in zip(
                resp["hourly"]["time"],
                resp["hourly"]["temperature_2m"],
                resp["hourly"]["apparent_temperature"],
                resp["hourly"]["rain"],
                resp["hourly"]["weathercode"],
                resp["hourly"]["cloudcover"],
            ):
                # this is bad! optimise later!
                Weather.objects.update_or_create(
                    date_time=time,
                    location=Point(lat, lon),
                    defaults={
                        "temperature": temp,
                        "apparent_temperature": apparent_temp,
                        "rain": rain,
                        "cloud_cover": cloud_cover,
                        "weather_code": weather_code,
                        "is_forecast": time > now
                    },
                )
