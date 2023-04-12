# Generated by Django 4.1.5 on 2023-01-29 13:37

import django.utils.timezone
import timescale.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("plants", "0003_datatype_unique_chart_colour"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="DataType",
            new_name="Sensor",
        ),
        migrations.AlterField(
            model_name="datapoint",
            name="time",
            field=timescale.db.models.fields.TimescaleDateTimeField(
                default=django.utils.timezone.now, interval="5 minutes"
            ),
        ),
    ]