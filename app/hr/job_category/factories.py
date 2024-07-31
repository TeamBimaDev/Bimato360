<<<<<<< HEAD
import factory
from .models import BimaHrJobCategory


class BimaHrJobCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrJobCategory

    name = factory.Faker('name')
    description = factory.Faker('text')
    active = factory.Faker('boolean')
    category = None
=======
import factory
from .models import BimaHrJobCategory


class BimaHrJobCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrJobCategory

    name = factory.Faker('name')
    description = factory.Faker('text')
    active = factory.Faker('boolean')
    category = None
>>>>>>> origin/ma-branch
