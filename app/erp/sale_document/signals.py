from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from .models import BimaErpSaleDocument


@receiver(pre_save, sender=BimaErpSaleDocument)
def update_product_quantities(sender, instance, **kwargs):
    try:
        previous_instance = sender.objects.get(id=instance.id)
    except ObjectDoesNotExist:
        previous_instance = None

    def adjust_product_quantity(sale_document, operation):
        try:
            for sale_document_product in sale_document.bimaerpsaledocumentproduct_set.all():
                product = sale_document_product.product
                if sale_document.type.lower() == 'quote':
                    product.virtual_quantity = operation(product.virtual_quantity, sale_document_product.quantity)
                elif sale_document.type.lower() in ['order', 'invoice']:
                    product.virtual_quantity = operation(product.virtual_quantity, sale_document_product.quantity)
                    product.quantity = operation(product.quantity, sale_document_product.quantity)
                product.save()
        except:
            pass

    if previous_instance:
        # If status was "Confirmed" and then changed to "Canceled" or "Draft"
        if previous_instance.status.lower() == 'confirmed' and instance.status.lower() in ['canceled', 'draft']:
            adjust_product_quantity(instance, lambda x, y: x + y)  # Add the product quantity

        # If status was "Canceled" or "Draft" and then changed to "Confirmed"
        elif previous_instance.status.lower() in ['canceled', 'draft'] and instance.status.lower() == 'confirmed':
            adjust_product_quantity(instance, lambda x, y: x - y)  # Subtract the product quantity

    else:  # if it's a new instance
        if str(instance.status).lower() == 'confirmed':
            adjust_product_quantity(instance, lambda x, y: x - y)  # Subtract the product quantity
