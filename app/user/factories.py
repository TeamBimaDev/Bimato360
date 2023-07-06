from factory.django import DjangoModelFactory
from factory import Faker
from django.contrib.auth import get_user_model


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = Faker('email')
    password = Faker('password')