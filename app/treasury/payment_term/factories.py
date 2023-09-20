import factory
from .models import BimaTreasuryPaymentTerm, BimaTreasuryPaymentTermDetail
from factory.django import DjangoModelFactory
from common.enums.transaction_enum import get_payment_term_type, get_payment_term_custom_type
import random


class BimaTreasuryPaymentTermFactory(DjangoModelFactory):
    class Meta:
        model = BimaTreasuryPaymentTerm

    name = factory.Faker('name')
    active = factory.Faker('boolean')
    type = factory.Faker('random_element', elements=get_payment_term_type())
    note = factory.Faker('text')
    code = factory.Faker('name')
    is_system = factory.Faker('boolean')

    @factory.post_generation
    def payment_term_details(self, create, extracted, **kwargs):
        if create and self.type == 'CUSTOM':
            num_details = 2
            percentages = [random.randint(1, 100) for _ in range(num_details - 1)]
            percentages.append(100 - sum(percentages))

            BimaTreasuryPaymentTermDetailFactory.create_batch(num_details, payment_term=self,
                                                              percentage=factory.Iterator(percentages))

    @factory.post_generation
    def check_percentage_sum(self, create, extracted, **kwargs):
        if create and self.type == 'CUSTOM':
            print(f"Checking percentage sum for {self.name}")
            total_percentage = sum(detail.percentage for detail in self.payment_term_details.all())
            print(f"Total percentage: {total_percentage}")
            if total_percentage != 100:
                raise ValueError(
                    "La somme des pourcentages ne correspond pas à 100 % pour le terme de paiement personnalisé.")


class BimaTreasuryPaymentTermDetailFactory(DjangoModelFactory):
    class Meta:
        model = BimaTreasuryPaymentTermDetail

    payment_term = factory.SubFactory(BimaTreasuryPaymentTermFactory)
    percentage = factory.Faker('random_int', min=1, max=100)
    value = factory.Faker('random_element', elements=get_payment_term_custom_type())
