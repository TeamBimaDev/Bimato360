import factory
from common.enums.language import LanguageEnum
from core.currency.factories import BimaCoreCurrencyFactory

from .models import BimaCompany


class BimaCompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCompany

    name = factory.Faker('company')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    mobile = factory.Faker('phone_number')
    fax = factory.Faker('phone_number')
    website = factory.Faker('url')
    language = factory.Faker('random_element', elements=[choice[0] for choice in LanguageEnum.choices])
    currency = factory.SubFactory(BimaCoreCurrencyFactory)
    timezone = 'UTC'
    header_note = factory.Faker('text')
    footer_note = factory.Faker('text')
