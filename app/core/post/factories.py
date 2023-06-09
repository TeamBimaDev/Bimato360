import factory
from .models import BimaCorePost
from ..department.factories import BimaCoreDepartmentFactory


class BimaCorePostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCorePost

    name = factory.Sequence(lambda n: f"Post {n}")
    department = factory.SubFactory(BimaCoreDepartmentFactory)
