# Generated by Django 4.2 on 2023-04-16 19:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("weather", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="weather",
            old_name="apparent_temperate",
            new_name="apparent_temperature",
        ),
    ]
