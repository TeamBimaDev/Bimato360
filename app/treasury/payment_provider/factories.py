import factory
from .models import BimaTreasuryPaymentProvider
from factory.django import DjangoModelFactory
from factory import Sequence


class BimaTreasuryPaymentProviderFactory(DjangoModelFactory):
    class Meta:
        model = BimaTreasuryPaymentProvider

    name = Sequence(lambda n: f"Fournisseur{n}")
    active = factory.Faker('boolean')
    credentials = {}
    supports_tokenization = factory.Faker('boolean')
    supports_manual_capture = factory.Faker('boolean')
    supports_refunds = factory.Faker('boolean')
