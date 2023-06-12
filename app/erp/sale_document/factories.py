import factory
from .models import BimaErpSaleDocument, BimaErpSaleDocumentProduct
from common.enums.sale_document_enum import get_sale_document_status, \
    get_sale_document_types, get_sale_document_validity
from erp.partner.factories import BimaErpPartnerFactory
from erp.product.factories import BimaErpProductFactory



class BimaErpSaleDocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaErpSaleDocument

    numbers = factory.Sequence(lambda n: f"D-{n}")
    date = factory.Faker('date')
    status = factory.Faker('random_element', elements=get_sale_document_status())
    type = factory.Faker('random_element', elements=get_sale_document_types())
    partner = factory.SubFactory(BimaErpPartnerFactory)
    note = factory.Faker('text')
    private_note = factory.Faker('text')
    validity = factory.Faker('random_element', elements=get_sale_document_validity())
    payment_terms = factory.Faker('word')
    delivery_terms = factory.Faker('word')
    subtotal = factory.Faker('pydecimal', left_digits=5, right_digits=3, positive=True)
    taxes = factory.Faker('pydecimal', left_digits=5, right_digits=3, positive=True)
    discounts = factory.Faker('pydecimal', left_digits=5, right_digits=3, positive=True)
    total = factory.Faker('pydecimal', left_digits=5, right_digits=3, positive=True)

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for product_data in extracted:
                BimaErpSaleDocumentProductFactory.create(sale_document=self, **product_data)
        else:
            pass


class BimaErpSaleDocumentProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaErpSaleDocumentProduct

    sale_document = factory.SubFactory(BimaErpSaleDocumentFactory)
    product = factory.SubFactory(BimaErpProductFactory)
    quantity = factory.Faker('pydecimal', left_digits=5, right_digits=3, positive=True)
    unit_price = factory.Faker('pydecimal', left_digits=5, right_digits=3, positive=True)
    vat = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True, max_value=100)
    description = factory.Faker('text')
    discount = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True, max_value=100)
    total_price = factory.LazyAttribute(lambda obj: obj.quantity * obj.unit_price)
