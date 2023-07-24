import factory

from .models import BimaCoreSource


class BimaCoreSourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCoreSource
    name = factory.Faker('name')
    description = factory.Faker('word')