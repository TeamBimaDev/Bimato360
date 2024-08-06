<<<<<<< HEAD
from .models import BimaCoreBank
from factory import Faker, Sequence
import factory
class BimaCoreBankFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCoreBank

    name = Sequence(lambda n: f"Company {n}")
    email = Sequence(lambda n: f"email{n}@example.com")
    active = Faker('boolean')
=======
from .models import BimaCoreBank
from factory import Faker, Sequence
import factory
class BimaCoreBankFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCoreBank

    name = Sequence(lambda n: f"Company {n}")
    email = Sequence(lambda n: f"email{n}@example.com")
    active = Faker('boolean')
>>>>>>> origin/ma-branch
    bic = Sequence(lambda n: f"SWIFT{n}")