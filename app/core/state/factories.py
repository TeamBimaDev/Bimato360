import factory

from .models import BimaCoreState

from core.country.factories import BimaCoreCountryFactory


class BimaCoreStateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCoreState

    name = factory.Faker('state')
    code = factory.Faker('name')
    country = factory.SubFactory(BimaCoreCountryFactory)
