# Generated by Django 4.2 on 2023-05-01 08:04

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Zone",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=256)),
                ("location", django.contrib.gis.db.models.fields.PointField(srid=4326, blank=True, null=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(
            model_name="zone",
            index=models.Index(fields=["location"], name="zone_location_idx"),
        ),
        migrations.AddConstraint(
            model_name="zone",
            constraint=models.UniqueConstraint(fields=("user", "name"), name="unique_zone_name_for_user"),
        ),
    ]
