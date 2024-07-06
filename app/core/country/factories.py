import factory

from .models import BimaCoreCountry
from core.currency.factories import BimaCoreCurrencyFactory


class BimaCoreCountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCoreCountry

    name = factory.Sequence(lambda n: f'CountryName{n}')
    code = factory.Sequence(lambda n: f'CountryCode{n}')
    iso3 = factory.Faker('text')
    iso2 = factory.Faker('text')
    capital = factory.Faker('text')
    address_format = factory.Faker('word')
    phone_code = factory.Faker('random_int')
    vat_label = factory.Faker('word')
    zip_required = factory.Faker('boolean')
    currency = factory.SubFactory(BimaCoreCurrencyFactory)
