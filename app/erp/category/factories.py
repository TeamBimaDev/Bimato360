import factory

from .models import BimaErpCategory


class BimaErpCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaErpCategory
    name = factory.Faker('name')
    description = factory.Faker('text')
    active = factory.Faker('boolean')
    category = None