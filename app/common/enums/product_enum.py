from enum import Enum


class PriceCalculationMethod(Enum):
    MANUAL = 'Manual Price'
    PERCENTAGE = 'Price based on Percentage'


class ProductType(Enum):
    STOCKABLE_PRODUCT = 'Stockable Products'
    SERVICE_PRODUCTS = 'Service Products'
    PRODUCTION_PRODUCTS = 'Production Products'


class ProductStatus(Enum):
    ACTIVE = 'Active'
    OUT_OF_STOCK = 'Out of Stock:'
    IN_TRANSIT = 'In transit'
    DISCONTINUED = 'Discontinued'
    NOT_FOR_SALE = 'Not for sale'


def get_product_price_calculation_method():
    return [(prd.name, prd.value) for prd in PriceCalculationMethod]


def get_product_types():
    return [(prd.name, prd.value) for prd in ProductType]


def get_product_status():
    return [(prd.name, prd.value) for prd in ProductStatus]
