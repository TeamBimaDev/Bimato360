from enum import Enum
from django.utils.translation import gettext_lazy as _

class PriceCalculationMethod(Enum):
    MANUAL = _('Manual Price')
    PERCENTAGE = _('Price based on Percentage')


class ProductType(Enum):
    STOCKABLE_PRODUCT = _('Stockable Products')
    SERVICE_PRODUCTS = _('Service Products')
    PRODUCTION_PRODUCTS = _('Production Products')


class ProductStatus(Enum):
    ACTIVE = _('Active')
    OUT_OF_STOCK = _('Out of Stock:')
    IN_TRANSIT = _('In transit')
    DISCONTINUED = _('Discontinued')
    NOT_FOR_SALE = _('Not for sale')


def get_product_price_calculation_method():
    return [(prd.name, prd.value) for prd in PriceCalculationMethod]


def get_product_types():
    return [(prd.name, prd.value) for prd in ProductType]


def get_product_status():
    return [(prd.name, prd.value) for prd in ProductStatus]
