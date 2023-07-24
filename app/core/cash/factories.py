from factory.django import DjangoModelFactory
from factory import Faker
from .models import BimaCoreCash

class BimaCoreCashFactory(DjangoModelFactory):
    class Meta:
        model = BimaCoreCash

    name = Faker('company')
    active = Faker('boolean')