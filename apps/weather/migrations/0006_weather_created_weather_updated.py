# Generated by Django 4.2 on 2023-04-18 17:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("weather", "0005_alter_weather_is_forecast"),
    ]

    operations = [
        migrations.AddField(
            model_name="weather",
            name="created",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="weather",
            name="updated",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
