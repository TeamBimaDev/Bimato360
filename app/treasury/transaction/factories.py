import factory
from .models import BimaTreasuryTransaction
from factory.django import DjangoModelFactory

from cash.factories import BimaTreasuryCashFactory
from treasury.payment_method.factories import BimaTreasuryPaymentMethodFactory
from treasury.transaction_type.factories import BimaTreasuryTransactionTypeFactory
from erp.partner.factories import BimaErpPartnerFactory
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from treasury.bank_account.models import BimaTreasuryBankAccount
from common.enums.transaction_enum import get_transaction_nature_cash_or_bank, \
    get_transaction_direction_income_or_outcome


class BimaTreasuryTransactionFactory(DjangoModelFactory):
    class Meta:
        model = BimaTreasuryTransaction

    number = factory.Faker('unique.random_number', digits=6)
    nature = factory.Faker('random_element', elements=get_transaction_nature_cash_or_bank())
    direction = factory.Faker('random_element',
                              elements=get_transaction_direction_income_or_outcome())
    transaction_type = factory.SubFactory(BimaTreasuryTransactionTypeFactory)
    payment_method = factory.SubFactory(BimaTreasuryPaymentMethodFactory)
    cash = factory.SubFactory(BimaTreasuryCashFactory)
    partner = factory.SubFactory(BimaErpPartnerFactory)
    parent_type = ContentType.objects.get_for_model(BimaTreasuryBankAccount)
    parent_id = factory.SelfAttribute('bank_account')
    content_object = GenericForeignKey('parent_type', 'parent_id')
    note = factory.Faker('text')
    date = factory.Faker('date')
    expected_date = factory.Faker('date', end_datetime='+30d')
    amount = factory.Faker('pydecimal', left_digits=10, right_digits=3)
    remaining_amount = factory.Faker('pydecimal', left_digits=12, right_digits=3)
    reference = factory.Faker('text', max_nb_chars=64)
    transaction_source = None
    partner_bank_account_number = factory.Faker('numerify',
                                                text='##############')
