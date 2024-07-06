from django.db import models
from django.utils.translation import gettext_lazy as _

from core.abstract.models import AbstractModel

from common.enums.product_enum import get_product_types, \
    get_product_price_calculation_method, \
    get_product_status
from erp.category.models import BimaErpCategory
from erp.vat.models import BimaErpVat

from erp.unit_of_measure.models import BimaErpUnitOfMeasure


class BimaErpProduct(AbstractModel):
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name=_('Name'))
    reference = models.CharField(max_length=255, blank=False, null=False, unique=True, verbose_name=_('Reference'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    ean13 = models.CharField(max_length=64, blank=True, null=True, verbose_name=_('EAN13'))
    type = models.CharField(max_length=255, choices=get_product_types(), blank=False, null=False,
                            verbose_name=_('Type'))
    purchase_price = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True,
                                         verbose_name=_('Purchase Price'))
    sell_price = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True,
                                     verbose_name=_('Sell Price'))
    price_calculation_method = models.CharField(max_length=50, choices=get_product_price_calculation_method(),
                                                blank=False, null=False, verbose_name=_('Price Calculation Method'))
    sell_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                                          verbose_name=_('Sell Percentage'))
    category = models.ForeignKey(BimaErpCategory, on_delete=models.PROTECT, verbose_name=_('Category'))
    vat = models.ForeignKey(BimaErpVat, on_delete=models.PROTECT, verbose_name=_('VAT'))
    unit_of_measure = models.ForeignKey(BimaErpUnitOfMeasure, on_delete=models.PROTECT,
                                        verbose_name=_('Unit of Measure'))
    status = models.CharField(max_length=50, choices=get_product_status(), blank=False, null=False,
                              verbose_name=_('Status'))
    minimum_stock_level = models.PositiveIntegerField(blank=True, null=True, default=0,
                                                      verbose_name=_('Minimum Stock Level'))
    maximum_stock_level = models.PositiveIntegerField(blank=True, null=True, default=0,
                                                      verbose_name=_('Maximum Stock Level'))
    dimension = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Dimension'))
    weight = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Weight'))
    reorder_point = models.PositiveIntegerField(blank=True, null=True, default=0, verbose_name=_('Reorder Point'))
    lead_time = models.PositiveIntegerField(blank=True, null=True, default=0, verbose_name=_('Lead Time'))
    serial_number = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Serial Number'))
    quantity = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, default=0,
                                   verbose_name=_('Quantity'))
    virtual_quantity = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, default=0,
                                           verbose_name=_('Virtual Quantity'))

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()
