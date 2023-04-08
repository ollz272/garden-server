import datetime

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

    def test_plant_chart_data(self):
        obj = PlantFactory()
        sensor = SensorFactory(plant=obj)
        DataPointFactory(
            sensor=sensor,
            plant=obj,
            time=datetime.datetime(2023, 2, 20, 0, 0, 0),
            data=0,
        )
        DataPointFactory(
            sensor=sensor,
            plant=obj,
            time=datetime.datetime(2023, 2, 20, 1, 0, 0),
            data=1,
        )
        DataPointFactory(
            sensor=sensor,
            plant=obj,
            time=datetime.datetime(2023, 2, 20, 2, 0, 0),
            data=2,
        )
        DataPointFactory(
            sensor=sensor,
            plant=obj,
            time=datetime.datetime(2023, 2, 20, 3, 0, 0),
            data=3,
        )
        chart_data = obj.to_chart_data(
            time_from=datetime.datetime(2023, 2, 20, 1, 0, 0),
            time_to=datetime.datetime(2023, 2, 20, 2, 0, 0),
        )
        self.assertEqual(
            chart_data,
            {
                sensor.slug: {
                    "time": [
                        datetime.datetime(2023, 2, 20, 1, 0, 0, tzinfo=datetime.timezone.utc),
                        datetime.datetime(2023, 2, 20, 2, 0, 0, tzinfo=datetime.timezone.utc),
                    ],
                    "data": [1.0, 2.0],
                    "chart_title": f"Chart of {sensor.name}",
                    "element_id": f"chart-{sensor.slug}",
                    "unit": f"{sensor.unit}",
                    "colour": f"{sensor.colour}",
                    "sensor_id": sensor.id,
                    "plant_id": obj.id,
                }
            },
        )

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
            {
                "plant": plant.id,
                "sensor": sensor.id,
                "data": "YOUR DATA HERE - MUST BE A NUMBER!",
            },
        )


class TestDataPoint(TestCase):
    def test_factory(self):
        obj = DataPointFactory.create()
        self.assertIsNotNone(obj.id)

    def test_str(self):
        obj = DataPointFactory.create()
        self.assertEqual(str(obj), f"Data point for {obj.plant} at {obj.time}")
