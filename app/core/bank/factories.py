from .models import BimaCoreBank
from factory import Faker, Sequence
import factory
class BimaCoreBankFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCoreBank

    name = Sequence(lambda n: f"Company {n}")
    email = Sequence(lambda n: f"email{n}@example.com")
    active = Faker('boolean')
    bic = Sequence(lambda n: f"SWIFT{n}")