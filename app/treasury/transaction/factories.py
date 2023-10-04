import factory
from .models import BimaTreasuryTransaction
from factory.django import DjangoModelFactory

from treasury.cash.factories import BimaTreasuryCashFactory
from treasury.payment_method.factories import BimaTreasuryPaymentMethodFactory
from treasury.transaction_type.factories import BimaTreasuryTransactionTypeFactory
from erp.partner.factories import BimaErpPartnerFactory
from treasury.bank_account.models import BimaTreasuryBankAccount
from common.enums.transaction_enum import get_transaction_nature_cash_or_bank, \
    get_transaction_direction_income_or_outcome
from core.bank.factories import BimaCoreBankFactory
from core.currency.factories import BimaCoreCurrencyFactory


class BimaTreasuryBankAccountFactory(factory.Factory):
    class Meta:
        model = BimaTreasuryBankAccount

    name = factory.Faker('company')
    account_number = factory.Sequence(lambda n: f'Account-{n}')
    iban = factory.Faker('iban')
    bank = factory.SubFactory(BimaCoreBankFactory)
    currency = factory.SubFactory(BimaCoreCurrencyFactory)
    balance = factory.Faker('pydecimal', left_digits=12, right_digits=3, positive=True)
    account_holder_name = factory.Faker('name')
    active = factory.Faker('boolean')
    note = factory.Faker('paragraph')
    parent_type = None
    parent_id = None
    content_object = None


class BimaTreasuryTransactionFactory(DjangoModelFactory):
    class Meta:
        model = BimaTreasuryTransaction

    number = factory.Faker('random_number', digits=6)
    nature = factory.Faker('random_element', elements=get_transaction_nature_cash_or_bank())
    direction = factory.Faker('random_element', elements=get_transaction_direction_income_or_outcome())
    transaction_type = factory.SubFactory(BimaTreasuryTransactionTypeFactory)
    payment_method = factory.SubFactory(BimaTreasuryPaymentMethodFactory)
    cash = factory.SubFactory(BimaTreasuryCashFactory)
    partner = factory.SubFactory(BimaErpPartnerFactory)
    #bank_account = factory.SubFactory(BimaTreasuryBankAccountFactory)
    note = factory.Faker('text')
    date = factory.Faker('date')
    expected_date = factory.Faker('date', end_datetime='+30d')
    amount = factory.Faker('pydecimal', left_digits=10, right_digits=3)
    remaining_amount = factory.Faker('pydecimal', left_digits=12, right_digits=3)
    reference = factory.Faker('text', max_nb_chars=64)
    transaction_source = None
    partner_bank_account_number = factory.Faker('numerify', text='')
