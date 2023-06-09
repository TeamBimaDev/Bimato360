import factory
from .models import BimaCoreTag


class BimaCoreTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCoreTag

    name = factory.Faker('name')
