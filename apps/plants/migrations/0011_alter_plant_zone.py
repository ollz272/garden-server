# Generated by Django 4.2 on 2023-05-01 08:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("zones", "0002_make_plant_zones"),
        ("plants", "0010_plant_zone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plant",
            name="zone",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="zones.zone"),
        ),
    ]
