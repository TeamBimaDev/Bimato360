from django.db.models import Sum
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
    totals = sale_document.products.all().aggregate(
        subtotal=Sum('total_price'),
        total_discounts=Sum('discount'),
        total_taxes=Sum('vat')
    )
    sale_document.subtotal = totals['subtotal']
    sale_document.discounts = totals['total_discounts']
    sale_document.taxes = totals['total_taxes']
    sale_document.total = totals['subtotal'] - totals['total_discounts'] + totals['total_taxes']
    sale_document.save()
