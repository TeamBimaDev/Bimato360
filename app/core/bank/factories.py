from factory.django import DjangoModelFactory
from factory import Faker
from .models import BimaCoreBank

class BimaCoreBankFactory(DjangoModelFactory):
    class Meta:
        model = BimaCoreBank

    name = Faker('company')
    email = Faker('email')
    bic = Faker('swift')
