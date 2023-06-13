from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BimaErpSaleDocument


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


