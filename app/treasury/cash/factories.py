from factory import Faker
from factory.django import DjangoModelFactory
import factory
from .models import BimaTreasuryCash
from company.factories import BimaCompanyFactory


class BimaTreasuryCashFactory(DjangoModelFactory):
    class Meta:
        model = BimaTreasuryCash

    name = Faker('company')
    active = Faker('boolean')
    company = factory.SubFactory(BimaCompanyFactory)

