import factory
from .models import BimaCoreTag
from faker import Faker as BaseFaker


class BimaCoreTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCoreTag

    name = factory.Faker('name')
    color = factory.LazyFunction(lambda: BaseFaker().hex_color()[:6])
    parent = None
