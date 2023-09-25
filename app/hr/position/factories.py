import factory
from core.department.factories import BimaCoreDepartmentFactory

from .models import BimaHrPosition


class BimaHrPositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrPosition

    name = factory.Faker('name')
    description = factory.Faker('text')
    requirements = factory.Faker('text')
    responsibilities = factory.Faker('text')
    department = factory.SubFactory(BimaCoreDepartmentFactory)
