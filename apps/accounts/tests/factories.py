import factory
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Sequence(lambda n: "person{0}@email.com".format(n))
    email = factory.Sequence(lambda n: "person{0}@email.com".format(n))
    password = "test123"

    class Meta:
        model = User
