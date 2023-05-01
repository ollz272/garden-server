import logging

import requests
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from django.utils.timezone import datetime, now
from pytz import utc
from weather.models import Weather
from zones.models import Zone

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Command for populating weather into the database.

    Populated from https://open-meteo.com/
    """

    url = (
        "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&hourly=temperature_2m,apparent_temperature,"
        "rain,weathercode,cloudcover&past_days=7&forecast_days=7"
    )

    def get_weather_data(self, lat, lon):
        return requests.get(self.url.format(lat, lon)).json()

    def handle(self, *args, **options):
        # TODO get lat/lon from database.
        for lat, lon in Zone.objects.order_by("location").distinct("location"):
            self.stdout.write(f"Fetching data for {lat}, {lon}")
            resp = self.get_weather_data(lat, lon)
            time_now = now()
            weather_objs = []

            for time, temp, apparent_temp, rain, weather_code, cloud_cover in zip(
                resp["hourly"]["time"],
                resp["hourly"]["temperature_2m"],
                resp["hourly"]["apparent_temperature"],
                resp["hourly"]["rain"],
                resp["hourly"]["weathercode"],
                resp["hourly"]["cloudcover"],
            ):
                tz_aware_time = datetime.fromisoformat(time)
                tz_aware_time = utc.localize(tz_aware_time)
                weather_objs.append(
                    Weather(
                        date_time=tz_aware_time,
                        location=Point(lat, lon),
                        temperature=temp,
                        apparent_temperature=apparent_temp,
                        rain=rain,
                        cloud_cover=cloud_cover,
                        weather_code=weather_code,
                        is_forecast=tz_aware_time > time_now,
                    )
                )

            # Bulk insert them, updating where needed
            Weather.objects.bulk_create(
                weather_objs,
                update_conflicts=True,
                update_fields=[
                    "temperature",
                    "apparent_temperature",
                    "rain",
                    "cloud_cover",
                    "weather_code",
                    "is_forecast",
                ],
                unique_fields=["date_time", "location"],
            )
