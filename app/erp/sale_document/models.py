from django.db import models
from simple_history.models import HistoricalRecords
from django.db.models.signals import post_save



from common.enums.sale_document_enum import get_sale_document_status, \
    get_sale_document_types, get_sale_document_validity

from erp.partner.models import BimaErpPartner
from erp.product.models import BimaErpProduct

from core.abstract.models import AbstractModel


class BimaErpSaleDocumentProduct(AbstractModel):
    sale_document = models.ForeignKey('BimaErpSaleDocument', on_delete=models.CASCADE)
    product = models.ForeignKey('BimaErpProduct', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False)
    reference = models.CharField(max_length=255, blank=False, null=False)
    quantity = models.DecimalField(max_digits=18, decimal_places=3, blank=False, null=False)
    unit_price = models.DecimalField(max_digits=18, decimal_places=3, blank=False, null=False)
    vat = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)
        post_save.send(self.__class__, instance=self)

    def calculate_total_price(self):
        price = self.unit_price * self.quantity
        if self.vat:
            price += (price * self.vat) / 100
        if self.discount:
            price -= (price * self.discount) / 100
        return price


class BimaErpSaleDocument(AbstractModel):
    number = models.CharField(max_length=32, null=False, blank=False, unique=True)
    date = models.DateField(null=False, blank=False)
    status = models.CharField(max_length=128, null=False,
                              blank=False, default="DRAFT",
                              choices=get_sale_document_status())
    type = models.CharField(max_length=128, null=False,
                            blank=False, default="DRAFT",
                            choices=get_sale_document_types())

    partner = models.ForeignKey(BimaErpPartner, on_delete=models.PROTECT)
    note = models.TextField(blank=True, null=True)
    private_note = models.TextField(blank=True, null=True)
    validity = models.CharField(blank=True, null=True, choices=get_sale_document_validity())
    payment_terms = models.CharField(max_length=100, blank=True, null=True)
    delivery_terms = models.CharField(max_length=100, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    taxes = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    discounts = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    total = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    parents = models.ManyToManyField('self', blank=True)
    history = HistoricalRecords()
    products = models.ManyToManyField(BimaErpProduct, through=BimaErpSaleDocumentProduct)

    def calculate_and_update_total(self):
        total_price = sum(product.total_price for product in self.products.all())
        self.total = total_price
        self.save()

    @classmethod
    def create_from_parents(cls, parent_docs, **kwargs):
        new_doc = cls.objects.create(**kwargs)  # create a new document
        new_doc.parents.set(parent_docs)  # link the new document to its parents
        # copy products from parents
        for parent_doc in parent_docs:
            for product in parent_doc.products.all():
                BimaErpSaleDocumentProduct.objects.create(
                    sale_document=new_doc,
                    product=product.product,
                    quantity=product.quantity,
                    unit_price=product.unit_price,
                    vat=product.vat,
                    description=product.description,
                    discount=product.discount
                )
        new_doc.calculate_and_update_total()  # update the total
        return new_doc
