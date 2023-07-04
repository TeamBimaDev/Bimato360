import factory
from .models import BimaErpPurchaseDocument, BimaErpPurchaseDocumentProduct
from common.enums.purchase_document_enum import get_purchase_document_status, \
    get_purchase_document_types, get_purchase_document_validity
from erp.partner.factories import BimaErpPartnerFactory
from erp.product.factories import BimaErpProductFactory


class BimaErpPurchaseDocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaErpPurchaseDocument

    number = factory.Sequence(lambda n: f"D-{n}")
    date = factory.Faker('date')
    status = factory.Faker('random_element', elements=get_purchase_document_status())
    type = factory.Faker('random_element', elements=get_purchase_document_types())
    partner = factory.SubFactory(BimaErpPartnerFactory)
    note = factory.Faker('text')
    private_note = factory.Faker('text')
    validity = factory.Faker('random_element', elements=get_purchase_document_validity())
    payment_terms = factory.Faker('word')
    delivery_terms = factory.Faker('word')

    @factory.post_generation
    def purchase_document_products(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for purchase_document_product in extracted:
                BimaErpPurchaseDocumentProductFactory(
                    purchase_document=self,
                    product=purchase_document_product.product,
                    quantity=factory.Faker("random_int", min=1, max=100)
                )
        else:
            BimaErpPurchaseDocumentProductFactory(purchase_document=self)


class BimaErpPurchaseDocumentProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaErpPurchaseDocumentProduct

    purchase_document = factory.SubFactory(BimaErpPurchaseDocumentFactory)
    product = factory.SubFactory(BimaErpProductFactory)
    purchase_document_public_id = factory.Faker("uuid4")
    name = factory.Faker("word")
    reference = factory.Faker("word")
    quantity = factory.Faker("random_int", min=1, max=100)
    unit_price = factory.Faker("pydecimal", left_digits=4, right_digits=3, positive=True)
    vat = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    description = factory.Faker("sentence")
    discount = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    total_without_vat = factory.Faker("pydecimal", left_digits=5, right_digits=3, positive=True)
    total_after_discount = factory.Faker("pydecimal", left_digits=5, right_digits=3, positive=True)
    total_price = factory.Faker("pydecimal", left_digits=5, right_digits=3, positive=True)
