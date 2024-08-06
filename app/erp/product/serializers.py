

from rest_framework import serializers
from .models import BimaErpProduct
from core.abstract.serializers import AbstractSerializer
from core.department.models import BimaCoreDepartment

from erp.category.models import BimaErpCategory
from erp.vat.models import BimaErpVat

from erp.unit_of_measure.models import BimaErpUnitOfMeasure


class BimaErpProductSerializer(AbstractSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    category_public_id = serializers.SlugRelatedField(
        queryset=BimaErpCategory.objects.all(),
        slug_field='public_id',
        source='category',
        write_only=True
    )

    def get_category(self, obj):
        return {
            'id': obj.category.public_id.hex,
            'name': obj.category.name,
        }

    vat = serializers.SerializerMethodField(read_only=True)
    vat_public_id = serializers.SlugRelatedField(
        queryset=BimaErpVat.objects.all(),
        slug_field='public_id',
        source='vat',
        write_only=True
    )

    def get_vat(self, obj):
        return {
            'id': obj.vat.public_id.hex,
            'name': obj.vat.name,
            'rate': obj.vat.rate,
        }

    unit_of_measure = serializers.SerializerMethodField(read_only=True)
    unit_of_measure_public_id = serializers.SlugRelatedField(
        queryset=BimaErpUnitOfMeasure.objects.all(),
        slug_field='public_id',
        source='unit_of_measure',
        write_only=True
    )

    def get_unit_of_measure(self, obj):
        return {
            'id': obj.unit_of_measure.public_id.hex,
            'name': obj.unit_of_measure.name,
        }

    class Meta:
        model = BimaErpProduct
        fields = [
            'id', 'name', 'reference', 'description', 'ean13', 'type', 'purchase_price', 'sell_price',
            'price_calculation_method', 'sell_percentage', 'status', 'minimum_stock_level', 'maximum_stock_level',
            'dimension', 'weight', 'reorder_point', 'lead_time', 'serial_number', 'category', 'category_public_id',
            'vat', 'vat_public_id', 'unit_of_measure', 'unit_of_measure_public_id', 'created', 'updated',
            'quantity', 'virtual_quantity'
        ]
        read_only_fields = ('quantity', 'virtual_quantity',)


