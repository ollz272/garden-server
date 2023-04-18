from django.db import migrations
from django.utils.timezone import now


def update_weather(apps, schema_editor):
    Weather = apps.get_model("weather", "Weather")
    for weather in Weather.objects.all():
        weather.is_forecast = weather.date_time > now()
        weather.save()


class Migration(migrations.Migration):
    dependencies = [
        ("weather", "0003_weather_is_forecast"),
    ]

    operations = [migrations.RunPython(update_weather)]
