from factory.django import DjangoModelFactory
from factory import Faker
from django.contrib.auth import get_user_model
from .models import BimaCoreBank


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = Faker('email')
    password = Faker('password')


class BimaCoreBankFactory(DjangoModelFactory):
    class Meta:
        model = BimaCoreBank

    name = Faker('company')
    email = Faker('email')
    bic = Faker('swift')
