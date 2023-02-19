from accounts.tests.factories import UserFactory
from django.test import TestCase


class TestUserModel(TestCase):
    def test_create(self):
        user = UserFactory()
        self.assertIsNotNone(user.id)
        self.assertIsNotNone(user.auth_token)
