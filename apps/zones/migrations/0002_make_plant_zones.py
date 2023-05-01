from django.db import migrations


def set_plant_zone(apps, schema_editor):
    Zone = apps.get_model("zones", "Zone")
    Plant = apps.get_model("plants", "Plant")
    # Set the partners' region as the needs region as a default.
    for plant in Plant.objects.all():
        if plant.indoor:
            zone = Zone.objects.get_or_create(user=plant.user, name="indoor")

        else:
            zone = Zone.objects.get_or_create(user=plant.user, name="outdoor")

        plant.zone = zone
        plant.save()


class Migration(migrations.Migration):
    dependencies = [
        ("zones", "0001_initial"),
        ("plants", "0010_plant_zone"),
    ]

    operations = [
        migrations.RunPython(set_plant_zone),
    ]
