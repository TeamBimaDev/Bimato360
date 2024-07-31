<<<<<<< HEAD
import factory
from .models import BimaCoreDepartment


class BimaCoreDepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCoreDepartment

    name = factory.Faker('name')
    description = factory.Faker('text')
    manager = factory.Faker("random_int", min=1, max=1000)
    department = None
=======
import factory
from .models import BimaCoreDepartment


class BimaCoreDepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCoreDepartment

    name = factory.Faker('name')
    description = factory.Faker('text')
    manager = factory.Faker("random_int", min=1, max=1000)
    department = None
>>>>>>> origin/ma-branch
