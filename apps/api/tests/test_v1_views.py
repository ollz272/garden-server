import datetime

from accounts.tests.factories import UserFactory
from django.test import TestCase
from django.urls import reverse
from plants.tests.factories import PlantFactory, SensorFactory, DataPointFactory


class TestPlantListAPIView(TestCase):
    def setUp(self):
        self.super_user = UserFactory(is_superuser=True)
        self.other_user = UserFactory()
        self.plants = PlantFactory.create_batch(5, user=self.super_user)
        PlantFactory.create_batch(5, user=self.other_user)

    def test_view_200(self):
        self.client.force_login(self.other_user)
        url = "v1-plants-list"
        resp = self.client.get(reverse(url))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 5)

    def test_view_200_super_user(self):
        self.client.force_login(self.super_user)
        url = "v1-plants-list"
        resp = self.client.get(reverse(url))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 10)

    def test_view_401_unauthenticated(self):
        self.client.logout()
        url = "v1-plants-list"
        resp = self.client.get(reverse(url))
        self.assertEqual(resp.status_code, 401)

    def test_view_200_queries(self):
        url = "v1-plants-list"
        self.client.force_login(self.super_user)
        with self.assertNumQueries(5):
            resp = self.client.get(reverse(url))
        self.assertEqual(resp.status_code, 200)


class TestPlantDetailAPIView(TestCase):
    def setUp(self):
        self.super_user = UserFactory(is_superuser=True)
        self.other_user = UserFactory()
        self.super_user_plant = PlantFactory(user=self.super_user)
        self.other_user_plant = PlantFactory(user=self.other_user)

    def test_view_200(self):
        self.client.force_login(self.other_user)
        url = "v1-plants-detail"
        resp = self.client.get(reverse(url, kwargs={"pk": self.other_user_plant.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_view_404_plant_belongs_to_other_user(self):
        self.client.force_login(self.other_user)
        url = "v1-plants-detail"
        resp = self.client.get(reverse(url, kwargs={"pk": self.super_user_plant.pk}))
        self.assertEqual(resp.status_code, 404)

    def test_view_200_super_user_can_get_all_plants(self):
        self.client.force_login(self.super_user)
        url = "v1-plants-detail"
        resp = self.client.get(reverse(url, kwargs={"pk": self.super_user_plant.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_view_401_unauthenticated(self):
        url = "v1-plants-detail"
        resp = self.client.get(reverse(url, kwargs={"pk": self.super_user_plant.pk}))
        self.assertEqual(resp.status_code, 401)


class TestPlantSensors(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.plant = PlantFactory(user=self.user)
        self.sensor = SensorFactory(plant=self.plant)
        self.url = "v1-plants-get-sensors"

    def test_get_sensors_200(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse(self.url, kwargs={"pk": self.plant.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.json(),
            [
                {
                    "id": self.sensor.id,
                    "name": self.sensor.name,
                    "plant": self.sensor.plant_id,
                    "plant_data": [],
                    "slug": self.sensor.slug,
                    "colour": self.sensor.colour,
                    "unit": self.sensor.unit,
                }
            ],
        )


class TestPlantCharts(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.plant = PlantFactory(user=self.user)
        self.sensor = SensorFactory(plant=self.plant)
        DataPointFactory(sensor=self.sensor, plant=self.plant, time=datetime.datetime(2023, 2, 20, 0, 0, 0), data=0)
        DataPointFactory(sensor=self.sensor, plant=self.plant, time=datetime.datetime(2023, 2, 20, 1, 0, 0), data=1)
        DataPointFactory(sensor=self.sensor, plant=self.plant, time=datetime.datetime(2023, 2, 20, 2, 0, 0), data=2)
        DataPointFactory(sensor=self.sensor, plant=self.plant, time=datetime.datetime(2023, 2, 20, 3, 0, 0), data=3)
        self.url = "v1-plants-charts"

    def test_get_sensors_200(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse(self.url, kwargs={"pk": self.plant.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.json(),
            {
                self.sensor.slug: {
                    "time": [
                        "2023-02-20T00:00:00Z",
                        "2023-02-20T01:00:00Z",
                        "2023-02-20T02:00:00Z",
                        "2023-02-20T03:00:00Z",
                    ],
                    "data": [0.0, 1.0, 2.0, 3.0],
                    "chart_title": f"Chart of {self.sensor.name}",
                    "element_id": f"chart-{self.sensor.slug}",
                    "unit": f"{self.sensor.unit}",
                    "colour": f"{self.sensor.colour}",
                    "sensor_id": self.sensor.id,
                    "plant_id": self.plant.id,
                }
            },
        )


class TestPlantCreateSensor(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.plant = PlantFactory(user=self.user)
        self.url = "v1-plants-create-sensor"

    def test_create_sensor_200(self):
        self.client.force_login(self.user)
        resp = self.client.post(reverse(self.url, kwargs={"pk": self.plant.pk}))
        self.assertEqual(resp.status_code, 200)

