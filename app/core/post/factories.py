import factory
from .models import BimaCorePost
from core.department.factories import BimaCoreDepartmentFactory


class BimaCorePostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCorePost

    name = factory.Faker('name')
    description = factory.Faker('text')
    requirements = factory.Faker('text')
    responsibilities = factory.Faker('text')
    department = factory.SubFactory(BimaCoreDepartmentFactory)

