from django.db import models

from core.abstract.models import AbstractModel

from common.enums.product_enum import get_product_types, \
    get_product_price_calculation_method, \
    get_product_status
from erp.category.models import BimaErpCategory
from erp.vat.models import BimaErpVat

from erp.unit_of_measure.models import BimaErpUnitOfMeasure


class BimaErpProduct(AbstractModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    reference = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    ean13 = models.CharField(max_length=64, blank=True, null=True)
    type = models.CharField(max_length=255, choices=get_product_types(), blank=False, null=False)
    purchase_price = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    sell_price = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    price_calculation_method = models.CharField(max_length=50,
                                                choices=get_product_price_calculation_method(), blank=False, null=False)
    sell_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(BimaErpCategory, on_delete=models.PROTECT)
    vat = models.ForeignKey(BimaErpVat, on_delete=models.PROTECT)
    unit_of_measure = models.ForeignKey(BimaErpUnitOfMeasure, on_delete=models.PROTECT)
    status = models.CharField(max_length=50, choices=get_product_status(), blank=False, null=False)
    minimum_stock_level = models.PositiveIntegerField(blank=True, null=True, default=0)
    maximum_stock_level = models.PositiveIntegerField(blank=True, null=True, default=0)
    dimension = models.CharField(max_length=255, blank=True, null=True)
    weight = models.CharField(max_length=255, blank=True, null=True)
    reorder_point = models.PositiveIntegerField(blank=True, null=True, default=0)
    lead_time = models.PositiveIntegerField(blank=True, null=True, default=0)
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    virtual_quantity = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)

    class Meta:
        ordering = ['name']
        permissions = []
