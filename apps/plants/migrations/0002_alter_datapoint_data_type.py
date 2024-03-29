# Generated by Django 4.0.4 on 2022-06-04 14:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plants", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="datapoint",
            name="data_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="plant_data",
                to="plants.datatype",
            ),
        ),
    ]
