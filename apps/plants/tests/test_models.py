from accounts.tests.factories import UserFactory
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from plants.tests.factories import DataPointFactory, PlantFactory, SensorFactory


class PlantTest(TestCase):
    def test_factory(self):
        obj = PlantFactory.create()
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.slug, slugify(obj.name, allow_unicode=True))

    def test_unique_constraint(self):
        user = UserFactory()
        PlantFactory.create(user=user, name="test")
        with self.assertRaises(IntegrityError):
            PlantFactory.create(user=user, name="test")

    def test_str(self):
        obj = PlantFactory.create()
        self.assertEqual(str(obj), obj.name)


class SensorTest(TestCase):
    def test_factory(self):
        obj = SensorFactory.create()
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.slug, slugify(obj.name, allow_unicode=True))

    def test_unique_constraint(self):
        plant = PlantFactory()
        SensorFactory.create(plant_id=plant.id, colour="test")
        with self.assertRaises(IntegrityError):
            SensorFactory.create(plant_id=plant.id, colour="test")

    def test_str(self):
        obj = SensorFactory.create()
        self.assertEqual(str(obj), obj.name)

    def test_api_url(self):
        obj = SensorFactory.create()
        self.assertEqual(obj.api_url, reverse("v1-plant-sensors-list"))

    def test_api_example_data(self):
        plant = PlantFactory()
        sensor = SensorFactory.create(plant=plant, colour="test")
        self.assertEqual(
            sensor.api_example_data,
            {"plant": plant.id, "sensor": sensor.id, "data": "YOUR DATA HERE - MUST BE A NUMBER!"},
        )


class TestDataPoint(TestCase):
    def test_factory(self):
        obj = DataPointFactory.create()
        self.assertIsNotNone(obj.id)

    def test_str(self):
        obj = DataPointFactory.create()
        self.assertEqual(str(obj), f"Data point for {obj.plant} at {obj.time}")
