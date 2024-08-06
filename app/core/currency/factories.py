import factory

from .models import BimaCoreCurrency


class BimaCoreCurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCoreCurrency

    name = factory.Sequence(lambda n: f'CurrencyName{n}')
    symbol = factory.Sequence(lambda n: f'CurrencySymbol{n}')
    decimal_places = factory.Faker('random_int')
    active = factory.Faker('boolean')
    currency_unit_label = factory.Faker('currency_code')
    currency_subunit_label = factory.Faker('word')
