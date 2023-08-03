from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .models import BimaErpSaleDocument
from django.utils.translation import gettext_lazy as _


class InsufficientQuantityError(Exception):
    def __init__(self, product):
        self.product = product
        super().__init__(f"Quantité insuffisante pour le produit {product.reference}")


def check_sale_document_contains_at_least_one_product_when_confirmed(instance):
    """Ensure that a confirmed SaleDocument contains at least one product."""
    if instance.status.lower() == "confirmed" and not instance.sale_document_products.exists():
        raise ValidationError(_("Confirmed Item must contain at least one Product."))


def update_product_quantities(sender, instance):
    try:
        previous_instance = sender.objects.get(id=instance.id)
    except ObjectDoesNotExist:
        previous_instance = None

    def adjust_product_quantity(sale_document, operation):
        try:
            for sale_document_product in sale_document.bimaerpsaledocumentproduct_set.all():
                product = sale_document_product.product
                if product.type == 'STOCKABLE_PRODUCT':
                    if sale_document.type.lower() == 'quote':
                        product.virtual_quantity = operation(product.virtual_quantity, sale_document_product.quantity)
                    elif sale_document.type.lower() in ['order', 'invoice']:
                        new_virtual_quantity = operation(product.virtual_quantity, sale_document_product.quantity)
                        new_quantity = operation(product.quantity, sale_document_product.quantity)
                        if new_quantity < 0:
                            raise InsufficientQuantityError(product)

                        product.virtual_quantity = new_virtual_quantity
                        product.quantity = new_quantity
                    elif sale_document.type.lower() == 'credit_note':
                        product.virtual_quantity = operation(product.virtual_quantity, -sale_document_product.quantity)
                        product.quantity = operation(product.quantity, -sale_document_product.quantity)
                    product.save()
        except InsufficientQuantityError as e:
            raise
        except:
            pass

    if previous_instance:
        # If status was "Confirmed" and then changed to "Canceled" or "Draft"
        if previous_instance.status.lower() == 'confirmed' and instance.status.lower() in ['canceled', 'draft']:
            adjust_product_quantity(instance, lambda x, y: x + y)  # Add the product quantity

        # If status was "Canceled" or "Draft" and then changed to "Confirmed"
        elif previous_instance.status.lower() in ['canceled', 'draft'] and instance.status.lower() == 'confirmed':
            adjust_product_quantity(instance, lambda x, y: x - y)  # Subtract the product quantity


@receiver(pre_save, sender=BimaErpSaleDocument)
def pre_save_sale_document(sender, instance, **kwargs):
    check_sale_document_contains_at_least_one_product_when_confirmed(instance)
    update_product_quantities(sender, instance)


@receiver(pre_delete, sender=BimaErpSaleDocument)
def check_products_before_delete(sender, instance, **kwargs):
    if instance.sale_document_products.count() > 0:
        raise ValidationError("Cannot delete item because it contains products.")
