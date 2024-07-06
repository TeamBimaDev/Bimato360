import factory
from .models import BimaErpUnitOfMeasure


class BimaErpUnitOfMeasureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaErpUnitOfMeasure
    name = factory.Faker('name')
    active = factory.Faker('boolean')
