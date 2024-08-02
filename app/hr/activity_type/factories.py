<<<<<<< HEAD
from .models import BimaHrActivityType
from factory import Faker
import factory


class BimaHrActivityTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrActivityType

    name = factory.Faker('name')
    description = factory.Faker('text')
    active = Faker('boolean')
=======
from .models import BimaHrActivityType
from factory import Faker
import factory


class BimaHrActivityTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrActivityType

    name = factory.Faker('name')
    description = factory.Faker('text')
    active = Faker('boolean')
>>>>>>> origin/ma-branch
