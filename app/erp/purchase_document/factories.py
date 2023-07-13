import factory
from .models import BimaErpPurchaseDocument, BimaErpPurchaseDocumentProduct
from common.enums.purchase_document_enum import get_purchase_document_status, \
    get_purchase_document_types, get_purchase_document_validity
from django.utils import timezone
from erp.partner.factories import BimaErpPartnerFactory
from erp.product.factories import BimaErpProductFactory

class BimaErpPurchaseDocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaErpPurchaseDocument

    number = factory.Sequence(lambda n: f'Document-{n}')
    number_at_partner = factory.Sequence(lambda n: f'Document-{n}-partner')
    date = factory.LazyFunction(timezone.now)
    status = factory.Faker('random_element', elements=get_purchase_document_status())
    type = factory.Faker('random_element', elements=get_purchase_document_types())
    partner = factory.SubFactory(BimaErpPartnerFactory)
    vat_label = factory.Faker('word')
    vat_amount = factory.Faker('pydecimal', left_digits=18, right_digits=3, positive=True)
    note = factory.Faker('text')
    private_note = factory.Faker('text')
    validity = factory.Faker('random_element', elements=get_purchase_document_validity())
    payment_terms = factory.Faker('word')
    delivery_terms = factory.Faker('word')
    total_amount_without_vat = factory.Faker('pydecimal', left_digits=18, right_digits=3, positive=True)
    total_after_discount = factory.Faker('pydecimal', left_digits=18, right_digits=3, positive=True)
    total_vat = factory.Faker('pydecimal', left_digits=18, right_digits=3, positive=True)
    total_amount = factory.Faker('pydecimal', left_digits=18, right_digits=3, positive=True)
    total_discount = factory.Faker('pydecimal', left_digits=18, right_digits=3, positive=True)
    is_recurring = factory.Faker('boolean')
    recurring_interval = factory.Faker('random_element', elements=(1, 2, 3))

    @factory.post_generation
    def purchase_document_products(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for product in extracted:
                BimaErpPurchaseDocumentProductFactory(purchase_document=self, product=product)

class BimaErpPurchaseDocumentProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaErpPurchaseDocumentProduct

    purchase_document = factory.SubFactory(BimaErpPurchaseDocumentFactory)
    product = factory.SubFactory(BimaErpProductFactory)
    purchase_document_public_id = factory.Faker('uuid4')
    name = factory.Sequence(lambda n: f'Product {n}')
    reference = factory.Sequence(lambda n: f'Reference {n}')
    quantity = factory.Faker('pydecimal', left_digits=18, right_digits=3, positive=True)
    unit_of_measure = 'default'
    unit_price = factory.Faker('pydecimal', left_digits=18, right_digits=3, positive=True)
    vat = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True, max_value=100)
    vat_amount = factory.Faker('pydecimal', left_digits=18, right_digits=3, positive=True)
    description = factory.Faker('text')
    discount = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True, max_value=100)
    discount_amount = factory.Faker('pydecimal', left_digits=18, right_digits=3, positive=True)
    total_without_vat = factory.Faker('pydecimal', left_digits=18, right_digits=3, positive=True)
    total_after_discount = factory.Faker('pydecimal', left_digits=18, right_digits=3, positive=True)
    total_price = factory.Faker('pydecimal', left_digits=18, right_digits=3, positive=True)
