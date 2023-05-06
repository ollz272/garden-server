import datetime

from accounts.tests.factories import UserFactory
from django.db import IntegrityError
from django.test import TestCase
from parameterized import parameterized
from plants.forms import PlantDataFilterForm, PlantForm, SensorForm
from plants.models import Plant, Sensor
from plants.tests.factories import DataPointFactory, PlantFactory, SensorFactory, SensorUnitFactory
from zones.tests.factories import ZoneFactory


class TestPlantForm(TestCase):
    def test_create_plant(self):
        user = UserFactory()
        zone = ZoneFactory(user=user)
        plant_form = PlantForm(user=user, data={"name": "test", "zone": zone.id})
        plant_form.save()

        self.assertTrue(Plant.objects.filter(name="test").exists())

    def test_create_plant_no_user(self):
        UserFactory()
        zone = ZoneFactory()
        plant_form = PlantForm(data={"name": "test", "zone": zone.id})

        with self.assertRaises(IntegrityError):
            plant_form.save()


class TestSensorForm(TestCase):
    def setUp(self) -> None:
        self.sensor_unit = SensorUnitFactory()

    def test_create_sensor(self):
        plant = PlantFactory()
        sensor_form = SensorForm(
            plant=plant,
            data={"name": "test", "unit": self.sensor_unit.id, "colour": "test"},
        )
        sensor_form.save()

        self.assertTrue(Sensor.objects.filter(name="test").exists())
        self.assertTrue(Sensor.objects.get(name="test").plant == plant)

    def test_create_sensor_no_plant(self):
        sensor_form = SensorForm(data={"name": "test", "unit": self.sensor_unit.id, "colour": "test"})
        with self.assertRaises(IntegrityError):
            sensor_form.save()


class TestPlantDataFilterForm(TestCase):
    def setUp(self) -> None:
        self.plant = PlantFactory()
        self.sensor = SensorFactory(plant=self.plant)
        DataPointFactory(
            sensor=self.sensor,
            plant=self.plant,
            time=datetime.datetime(2023, 2, 20, 0, 0, 0),
            data=0,
        )
        DataPointFactory(
            sensor=self.sensor,
            plant=self.plant,
            time=datetime.datetime(2023, 2, 20, 1, 0, 0),
            data=1,
        )
        DataPointFactory(
            sensor=self.sensor,
            plant=self.plant,
            time=datetime.datetime(2023, 2, 20, 2, 0, 0),
            data=2,
        )
        DataPointFactory(
            sensor=self.sensor,
            plant=self.plant,
            time=datetime.datetime(2023, 2, 20, 3, 0, 0),
            data=3,
        )

    def test_form_data_validator(self):
        form = PlantDataFilterForm(
            self.plant,
            data={
                "start_date": datetime.datetime(2023, 2, 20, 2, 0, 0),
                "end_date": datetime.datetime(2023, 2, 20, 1, 0, 0),
            },
        )
        self.assertFalse(form.is_valid())

    def test_form_to_chart_data(self):
        form = PlantDataFilterForm(
            self.plant,
            data={
                "start_date": datetime.datetime(2023, 2, 20, 1, 0, 0),
                "end_date": datetime.datetime(2023, 2, 20, 2, 0, 0),
                "resolution": "PT1S",
            },
        )

        form.is_valid()

        self.assertEqual(
            form.chart_data(),
            {
                self.sensor.slug: {
                    "time": [
                        datetime.datetime(2023, 2, 20, 1, 0, 0, tzinfo=datetime.timezone.utc),
                        datetime.datetime(2023, 2, 20, 2, 0, 0, tzinfo=datetime.timezone.utc),
                    ],
                    "data": [1.0, 2.0],
                    "chart_title": f"Chart of {self.sensor.name}",
                    "element_id": f"chart-{self.sensor.slug}",
                    "unit": f"{self.sensor.unit}",
                    "colour": f"{self.sensor.colour}",
                    "sensor_id": self.sensor.id,
                    "plant_id": self.plant.id,
                }
            },
        )

    @parameterized.expand(("PT1S", "PT1M", "PT60M", "P1D"))
    def test_form_to_chart_data_period(self, resolution):
        form = PlantDataFilterForm(
            self.plant,
            data={
                "start_date": datetime.datetime(2023, 2, 20, 1, 0, 0),
                "end_date": datetime.datetime(2023, 2, 20, 2, 0, 0),
                "resolution": resolution,
            },
        )

        form.is_valid()
        form.chart_data()
