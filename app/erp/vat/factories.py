import factory
from decimal import Decimal
from random import randint
from .models import BimaErpVat

class BimaErpVatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaErpVat

    name = factory.Faker('name')
    rate = factory.LazyFunction(lambda: Decimal(randint(1, 9999)) / 100)
    active = factory.Faker('boolean')
