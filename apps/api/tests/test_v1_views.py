from accounts.tests.factories import UserFactory
from django.test import TestCase
from django.urls import reverse
from plants.tests.factories import PlantFactory


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
        with self.assertNumQueries(4):
            resp = self.client.get(reverse(url))
        self.assertEqual(resp.status_code, 200)

    def test_view_200_csv(self):
        url = "v1-plants-plant-csv-data"
        self.client.force_login(self.super_user)
        resp = self.client.get(reverse(url))
        self.assertEqual(resp.status_code, 200)

        # todo test response.


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

    def test_view_200_csv(self):
        url = "v1-plants-individual-plant-csv-data"
        self.client.force_login(self.super_user)
        resp = self.client.get(reverse(url, kwargs={"pk": self.super_user_plant.pk}))
        self.assertEqual(resp.status_code, 200)

        # todo test response.
