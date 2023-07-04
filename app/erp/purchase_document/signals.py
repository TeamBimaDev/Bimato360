from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .models import BimaErpPurchaseDocument
from django.utils.translation import gettext_lazy as _


class InsufficientQuantityError(Exception):
    def __init__(self, product):
        self.product = product
        super().__init__(_(f"Insufficient quantity for product {product.reference}"))


def check_purchase_document_contains_at_least_one_product_when_confirmed(instance):
    """Ensure that a confirmed PurchaseDocument contains at least one product."""
    if instance.status.lower() == "confirmed" and not instance.purchase_document_products.exists():
        raise ValidationError(_("Confirmed Item must contain at least one Product."))


def update_product_quantities(sender, instance):
    try:
        previous_instance = sender.objects.get(id=instance.id)
    except ObjectDoesNotExist:
        previous_instance = None

    def adjust_product_quantity(purchase_document, operation):
        try:
            for purchase_document_product in purchase_document.bimaerppurchasedocumentproduct_set.all():
                product = purchase_document_product.product
                if purchase_document.type.lower() == 'quote':
                    product.virtual_quantity = operation(product.virtual_quantity, purchase_document_product.quantity)
                elif purchase_document.type.lower() in ['order', 'invoice']:
                    new_virtual_quantity = operation(product.virtual_quantity, purchase_document_product.quantity)
                    new_quantity = operation(product.quantity, purchase_document_product.quantity)
                    if new_quantity < 0:
                        raise InsufficientQuantityError(product)

                    product.virtual_quantity = new_virtual_quantity
                    product.quantity = new_quantity
                elif purchase_document.type.lower() == 'credit_note':
                    product.virtual_quantity = operation(product.virtual_quantity, -purchase_document_product.quantity)
                    product.quantity = operation(product.quantity, -purchase_document_product.quantity)
                product.save()
        except InsufficientQuantityError as e:
            print(_(f"Insufficient quantity for product {e.product.reference}"))
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


@receiver(pre_save, sender=BimaErpPurchaseDocument)
def pre_save_purchase_document(sender, instance, **kwargs):
    check_purchase_document_contains_at_least_one_product_when_confirmed(instance)
    update_product_quantities(sender, instance)


@receiver(pre_delete, sender=BimaErpPurchaseDocument)
def check_products_before_delete(sender, instance, **kwargs):
    if instance.purchase_document_products.count() > 0:
        raise ValidationError("Cannot delete item because it contains products.")