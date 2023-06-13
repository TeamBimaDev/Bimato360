from django.db.models import Sum, DecimalField, F, FloatField
from django.db.models.functions import Coalesce
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BimaErpSaleDocument, BimaErpSaleDocumentProduct


@receiver(post_save, sender=BimaErpSaleDocument)
def update_product_quantities(sender, instance, **kwargs):
    previous_instance = sender.objects.get(id=instance.id)

    def adjust_product_quantity(sale_document, operation):
        for sale_document_product in sale_document.sale_document_product_set.all():
            product = sale_document_product.product
            if sale_document.type == 'Quote':
                product.virtual_quantity = operation(product.virtual_quantity, sale_document_product.quantity)
            elif sale_document.type in ['Order', 'Invoice']:
                product.virtual_quantity = operation(product.virtual_quantity, sale_document_product.quantity)
                product.quantity = operation(product.quantity, sale_document_product.quantity)
            product.save()

    # If status was "Confirmed" and then changed to "Canceled" or "Draft"
    if previous_instance.status == 'Confirmed' and instance.status in ['Canceled', 'Draft']:
        adjust_product_quantity(instance, lambda x, y: x + y)  # Add the product quantity

    # If status is "Confirmed"
    elif instance.status == 'Confirmed':
        adjust_product_quantity(instance, lambda x, y: x - y)  # Subtract the product quantity


@receiver(post_save, sender=BimaErpSaleDocumentProduct)
def update_sale_document_totals(sender, instance, **kwargs):
    sale_document = instance.sale_document
    sale_document_products = BimaErpSaleDocumentProduct.objects.filter(sale_document=sale_document)
    totals = sale_document_products.aggregate(
        total_discounts=Sum('discount_amount', output_field=DecimalField()),
        total_taxes=Sum('vat_amount', output_field=DecimalField()),
        total_amount=Sum('total_price', output_field=DecimalField())
    )
    sale_document.total_discount = totals['total_discounts'] if totals['total_discounts'] else 0
    sale_document.total_vat = totals['total_taxes'] if totals['total_taxes'] else 0
    sale_document.total_amount = totals['total_amount'] if totals['total_amount'] else 0
    sale_document.save()
