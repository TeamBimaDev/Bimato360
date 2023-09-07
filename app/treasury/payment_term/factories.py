import factory
from .models import BimaTreasuryPaymentTerm
from factory.django import DjangoModelFactory
from common.enums.transaction_enum import get_payment_term_type


class BimaTreasuryPaymentTermFactory(DjangoModelFactory):
    class Meta:
        model = BimaTreasuryPaymentTerm

    name = factory.Faker('name')
    active = factory.Faker('boolean')
    type = factory.Faker('random_element', elements=get_payment_term_type())
    note = factory.Faker('text')
    code = factory.Faker('name')
    is_system = factory.Faker('boolean')

