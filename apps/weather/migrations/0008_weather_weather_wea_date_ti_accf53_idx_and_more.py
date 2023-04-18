# Generated by Django 4.2 on 2023-04-18 18:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("weather", "0007_alter_weather_weather_code"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="weather",
            index=models.Index(fields=["date_time"], name="weather_wea_date_ti_accf53_idx"),
        ),
        migrations.AddIndex(
            model_name="weather",
            index=models.Index(fields=["location"], name="weather_wea_locatio_ac2c7d_idx"),
        ),
        migrations.AddIndex(
            model_name="weather",
            index=models.Index(fields=["is_forecast"], name="weather_wea_is_fore_5efbe1_idx"),
        ),
        migrations.AddIndex(
            model_name="weather",
            index=models.Index(fields=["weather_code"], name="weather_wea_weather_26d322_idx"),
        ),
    ]
