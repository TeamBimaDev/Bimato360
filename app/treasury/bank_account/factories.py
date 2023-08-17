from factory import Faker
from factory.django import DjangoModelFactory

from .models import BimaCoreCash


class BimaTreasuryCashFactory(DjangoModelFactory):
    class Meta:
        model = BimaCoreCash

    name = Faker('company')
    active = Faker('boolean')
