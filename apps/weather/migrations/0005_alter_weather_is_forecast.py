# Generated by Django 4.2 on 2023-04-18 17:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("weather", "0004_set_default_weather"),
    ]

    operations = [
        migrations.AlterField(
            model_name="weather",
            name="is_forecast",
            field=models.BooleanField(),
        ),
    ]
