<<<<<<< HEAD
import factory
from .models import BimaTreasuryPaymentMethod
from common.enums.transaction_enum import get_transaction_type_income_outcome, get_transaction_type_for_cash_or_bank
from factory.django import DjangoModelFactory


class BimaTreasuryPaymentMethodFactory(DjangoModelFactory):
    class Meta:
        model = BimaTreasuryPaymentMethod

    name = factory.Faker('name')
    active = factory.Faker('boolean')
    note = factory.Faker('text')
    code = factory.Faker('name')
    is_system = factory.Faker('boolean')
    income_outcome = factory.Faker('random_element', elements=get_transaction_type_income_outcome())
    cash_bank = factory.Faker('random_element', elements=get_transaction_type_for_cash_or_bank())
=======
import factory
from .models import BimaTreasuryPaymentMethod
from common.enums.transaction_enum import get_transaction_type_income_outcome, get_transaction_type_for_cash_or_bank
from factory.django import DjangoModelFactory


class BimaTreasuryPaymentMethodFactory(DjangoModelFactory):
    class Meta:
        model = BimaTreasuryPaymentMethod

    name = factory.Faker('name')
    active = factory.Faker('boolean')
    note = factory.Faker('text')
    code = factory.Faker('name')
    is_system = factory.Faker('boolean')
    income_outcome = factory.Faker('random_element', elements=get_transaction_type_income_outcome())
    cash_bank = factory.Faker('random_element', elements=get_transaction_type_for_cash_or_bank())
>>>>>>> origin/ma-branch
