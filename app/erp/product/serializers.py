from rest_framework import serializers
from .models import BimaErpProduct
from core.abstract.serializers import AbstractSerializer
from core.department.models import BimaCoreDepartment

from erp.category.models import BimaErpCategory
from erp.vat.models import BimaErpVat

from erp.unit_of_measure.models import BimaErpUnitOfMeasure


class BimaErpProductSerializer(AbstractSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=BimaErpCategory.objects.all(),
        source='category',
        write_only=True
    )

    def get_category(self, obj):
        return {
            'id': obj.category.public_id.hex,
            'name': obj.category.name,
        }

    vat = serializers.SerializerMethodField(read_only=True)
    vat_id = serializers.PrimaryKeyRelatedField(
        queryset=BimaErpVat.objects.all(),
        source='vat',
        write_only=True
    )

    def get_vat(self, obj):
        return {
            'id': obj.vat.public_id.hex,
            'name': obj.vat.name,
        }

    unit_of_measure = serializers.SerializerMethodField(read_only=True)
    unit_of_measure_id = serializers.PrimaryKeyRelatedField(
        queryset=BimaErpUnitOfMeasure.objects.all(),
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
            'dimension', 'weight', 'reorder_point', 'lead_time', 'serial_number', 'category', 'category_id', 'vat',
            'vat_id', 'unit_of_measure', 'unit_of_measure_id', 'created', 'updated'
        ]
