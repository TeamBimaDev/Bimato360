<<<<<<< HEAD
import factory

from .models import BimaCoreSource


class BimaCoreSourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCoreSource
    name = factory.Faker('name')
=======
import factory

from .models import BimaCoreSource


class BimaCoreSourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCoreSource
    name = factory.Faker('name')
>>>>>>> origin/ma-branch
    description = factory.Faker('word')