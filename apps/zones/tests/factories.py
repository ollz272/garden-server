import factory
from accounts.tests.factories import UserFactory
from factory.django import DjangoModelFactory
from zones import models


class ZoneFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"zone {n}")

    class Meta:
        model = models.Zone
