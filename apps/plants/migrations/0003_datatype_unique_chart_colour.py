# Generated by Django 4.0.6 on 2022-07-24 19:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plants", "0002_alter_datapoint_data_type"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="datatype",
            constraint=models.UniqueConstraint(fields=("plant", "colour"), name="unique_chart_colour"),
        ),
    ]
