import factory
from .models import BimaTreasuryRefund
from treasury.transaction.models import BimaTreasuryTransaction


class BimaTreasuryRefundFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaTreasuryRefund

    transaction = factory.SubFactory(BimaTreasuryTransaction)
    amount = factory.Faker('pydecimal', left_digits=18, right_digits=3)
    reason = factory.Faker('text')
    date = factory.Faker('date')
