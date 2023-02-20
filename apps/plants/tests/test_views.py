import datetime

from accounts.tests.factories import UserFactory
from django.test import TestCase
from django.urls import reverse
from django_webtest import WebTest
from plants.models import Plant, Sensor
from plants.tests.factories import PlantFactory, SensorFactory


class TestListPlantView(TestCase):
    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        other_user = UserFactory()
        self.client.force_login(self.user)
        self.url_name = "plant-list"
        self.plants = PlantFactory.create_batch(5, user=self.user)
        PlantFactory.create_batch(5, user=other_user)

    def test_list_plants_view(self):
        response = self.client.get(reverse(self.url_name))

        self.assertEqual(response.status_code, 200)

        # The list should only contain a users plants
        self.assertEqual(list(response.context["plants"]), self.plants)


class TestPlantCreateView(WebTest):
    def setUp(self) -> None:
        self.user = UserFactory(is_superuser=True)
        self.app.set_user(self.user)
        self.url_name = "plant-create"

    def test_create_plant_200(self):
        resp = self.app.get(reverse(self.url_name))
        self.assertEqual(resp.status_code, 200)

    def test_create_plant_301_submit_form(self):
        resp = self.app.get(reverse(self.url_name))
        form = resp.forms[0]
        form["name"] = "test"
        form["indoor"] = True
        resp = form.submit()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Plant.objects.count(), 1)
        plant = Plant.objects.get(name="test")
        self.assertEqual(plant.user, self.user)
        self.assertEqual(plant.indoor, True)
        self.assertEqual(plant.slug, "test")

    def test_create_plant_200_submit_form_error(self):
        resp = self.app.get(reverse(self.url_name))
        form = resp.forms[0]
        form["indoor"] = True
        resp = form.submit()
        self.assertEqual(resp.status_code, 200)


class TestPlantUpdateView(WebTest):
    def setUp(self) -> None:
        self.user = UserFactory(is_superuser=True)
        self.app.set_user(self.user)
        self.url_name = "plant-update"
        self.plant = PlantFactory(user=self.user)

    def test_update_plant_200(self):
        resp = self.app.get(reverse(self.url_name, kwargs={"plant_pk": self.plant.id}))
        self.assertEqual(resp.status_code, 200)

    def test_update_plant_404_plant_doesnt_belong_to_user(self):
        plant = PlantFactory()
        resp = self.app.get(reverse(self.url_name, kwargs={"plant_pk": plant.id}), expect_errors=True)
        self.assertEqual(resp.status_code, 404)

    def test_update_plant_301_submit_form(self):
        resp = self.app.get(reverse(self.url_name, kwargs={"plant_pk": self.plant.id}))
        form = resp.forms[0]
        form["name"] = "test"
        form["indoor"] = True
        resp = form.submit()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Plant.objects.count(), 1)
        plant = Plant.objects.get(id=self.plant.id)
        self.assertEqual(plant.user, self.user)
        self.assertEqual(plant.indoor, True)
        self.assertEqual(plant.slug, "test")

    def test_update_plant_200_submit_form_error(self):
        resp = self.app.get(reverse(self.url_name, kwargs={"plant_pk": self.plant.id}))
        form = resp.forms[0]
        form["indoor"] = True
        form["name"] = ""
        resp = form.submit()
        self.assertEqual(resp.status_code, 200)


class TestPlantChartView(WebTest):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.user = UserFactory(is_superuser=True)
        self.app.set_user(self.user)
        self.url_name = "plant-chart"
        self.plant = PlantFactory(user=self.user)

    def test_plant_chart_200(self):
        resp = self.app.get(reverse(self.url_name, kwargs={"plant_pk": self.plant.id}))
        self.assertEqual(resp.status_code, 200)

    def test_plant_chart_200_query_params(self):
        resp = self.app.get(
            reverse(self.url_name, kwargs={"plant_pk": self.plant.id}),
            params={
                "start_date": datetime.datetime(2023, 2, 20, 0, 0, 0),
                "end_date": datetime.datetime(2023, 2, 21, 0, 0, 0),
            },
        )
        self.assertEqual(resp.status_code, 200)

    def test_plant_chart_200_super_user(self):
        user = UserFactory(is_superuser=True)
        self.app.set_user(user)
        resp = self.app.get(reverse(self.url_name, kwargs={"plant_pk": self.plant.id}))
        self.assertEqual(resp.status_code, 200)


class TestApiInfoView(WebTest):
    def setUp(self) -> None:
        self.user = UserFactory(is_superuser=True)
        self.app.set_user(self.user)
        self.url_name = "plant-api-details"
        self.plant = PlantFactory(user=self.user)
        self.sensor = SensorFactory(plant=self.plant)

    def test_api_detail_view_200(self):
        resp = self.app.get(reverse(self.url_name, kwargs={"plant_pk": self.plant.id}))
        self.assertEqual(resp.status_code, 200)


class TestCreateSensorView(WebTest):
    def setUp(self) -> None:
        self.user = UserFactory(is_superuser=True)
        self.app.set_user(self.user)
        self.url_name = "create-sensor"
        self.plant = PlantFactory(user=self.user)

    def test_create_sensor_200(self):
        resp = self.app.get(reverse(self.url_name, kwargs={"plant_pk": self.plant.id}))
        self.assertEqual(resp.status_code, 200)

    def test_create_sensor_404_no_access(self):
        plant = PlantFactory()
        resp = self.app.get(reverse(self.url_name, kwargs={"plant_pk": plant.id}), expect_errors=True)
        self.assertEqual(resp.status_code, 404)

    def test_update_plant_301_submit_form(self):
        resp = self.app.get(reverse(self.url_name, kwargs={"plant_pk": self.plant.id}))
        form = resp.forms[0]
        form["name"] = "test"
        form["unit"] = "test"
        form["colour"] = "test"
        resp = form.submit()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Sensor.objects.count(), 1)
        sensor = Sensor.objects.get(name="test")
        self.assertEqual(sensor.plant, self.plant)
        self.assertEqual(sensor.name, "test")
        self.assertEqual(sensor.unit, "test")
        self.assertEqual(sensor.colour, "test")

    def test_update_plant_200_submit_form_error(self):
        resp = self.app.get(reverse(self.url_name, kwargs={"plant_pk": self.plant.id}))
        form = resp.forms[0]
        form["name"] = ""
        form["unit"] = ""
        form["colour"] = ""
        resp = form.submit()
        self.assertEqual(resp.status_code, 200)


class TestUpdateSensorView(WebTest):
    def setUp(self) -> None:
        self.user = UserFactory(is_superuser=True)
        self.app.set_user(self.user)
        self.url_name = "update-sensor"
        self.plant = PlantFactory(user=self.user)
        self.sensor = SensorFactory(plant=self.plant)

    def test_update_sensor_200(self):
        resp = self.app.get(reverse(self.url_name, kwargs={"plant_pk": self.plant.id, "sensor_pk": self.sensor.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_create_sensor_404_no_access_to_plant(self):
        plant = PlantFactory()
        sensor = SensorFactory(plant=plant)
        resp = self.app.get(
            reverse(self.url_name, kwargs={"plant_pk": plant.id, "sensor_pk": sensor.id}), expect_errors=True
        )
        self.assertEqual(resp.status_code, 404)

    def test_create_sensor_404_sensor_doesnt_belong_to_plant(self):
        sensor = SensorFactory()
        resp = self.app.get(
            reverse(self.url_name, kwargs={"plant_pk": self.plant.id, "sensor_pk": sensor.id}), expect_errors=True
        )
        self.assertEqual(resp.status_code, 404)

    def test_update_plant_301_submit_form(self):
        resp = self.app.get(reverse(self.url_name, kwargs={"plant_pk": self.plant.id, "sensor_pk": self.sensor.id}))
        form = resp.forms[0]
        form["name"] = "test"
        form["unit"] = "test"
        form["colour"] = "test"
        resp = form.submit()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Sensor.objects.count(), 1)
        sensor = Sensor.objects.get(name="test")
        self.assertEqual(sensor.plant, self.plant)
        self.assertEqual(sensor.name, "test")
        self.assertEqual(sensor.unit, "test")
        self.assertEqual(sensor.colour, "test")

    def test_update_plant_200_submit_form_error(self):
        resp = self.app.get(reverse(self.url_name, kwargs={"plant_pk": self.plant.id, "sensor_pk": self.sensor.id}))
        form = resp.forms[0]
        form["name"] = ""
        form["unit"] = ""
        form["colour"] = ""
        resp = form.submit()
        self.assertEqual(resp.status_code, 200)
