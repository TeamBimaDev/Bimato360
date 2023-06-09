import factory
from .models import BimaCoreBank


class BimaCoreBankFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCoreBank
    name = factory.Faker('name')
    email = factory.Faker('email')
    active = factory.Faker('boolean')
    bic = factory.Faker('word')
