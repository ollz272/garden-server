from accounts.tests.factories import UserFactory
from django.db import IntegrityError
from django.test import TestCase
from plants.forms import PlantForm, SensorForm
from plants.models import Plant, Sensor
from plants.tests.factories import PlantFactory


class TestPlantForm(TestCase):
    def test_create_plant(self):
        user = UserFactory()
        plant_form = PlantForm(user=user, data={"name": "test", "indoor": True})
        plant_form.save()

        self.assertTrue(Plant.objects.filter(name="test").exists())

    def test_create_plant_no_user(self):
        user = UserFactory()
        plant_form = PlantForm(data={"name": "test", "indoor": True})

        with self.assertRaises(IntegrityError):
            plant_form.save()


class TestSensorForm(TestCase):
    def test_create_sensor(self):
        plant = PlantFactory()
        sensor_form = SensorForm(plant=plant, data={"name": "test", "unit": "test", "colour": "test"})
        sensor_form.save()

        self.assertTrue(Sensor.objects.filter(name="test").exists())
        self.assertTrue(Sensor.objects.get(name="test").plant == plant)

    def test_create_sensor_no_plant(self):
        sensor_form = SensorForm(data={"name": "test", "unit": "test", "colour": "test"})
        with self.assertRaises(IntegrityError):
            sensor_form.save()
