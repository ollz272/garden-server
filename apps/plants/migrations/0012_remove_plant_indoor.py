# Generated by Django 4.2 on 2023-05-01 13:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("plants", "0011_alter_plant_zone"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="plant",
            name="indoor",
        ),
    ]
