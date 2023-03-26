import datetime as dt

import factory
from accounts.tests.factories import UserFactory
from factory.django import DjangoModelFactory
from plants import models


class PlantFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"plant {n}")
    indoor = True

    class Meta:
        model = models.Plant


class SensorUnitFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"unit {n}")

    class Meta:
        model = models.SensorUnit


class SensorFactory(DjangoModelFactory):
    plant = factory.SubFactory(PlantFactory)
    name = factory.Sequence(lambda n: f"sensor {n}")
    unit = factory.SubFactory(SensorUnitFactory)
    colour = "..."

    class Meta:
        model = models.Sensor


class DataPointFactory(DjangoModelFactory):
    plant = factory.SubFactory(PlantFactory)
    sensor = factory.SubFactory(SensorFactory)
    time = dt.date.today()
    data = 10

    class Meta:
        model = models.DataPoint
