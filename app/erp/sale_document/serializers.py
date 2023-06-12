from rest_framework import serializers

from core.abstract.serializers import AbstractSerializer

from erp.product.models import BimaErpProduct
from .models import BimaErpSaleDocument, BimaErpSaleDocumentProduct


class BimaErpSaleDocumentSerializer(AbstractSerializer):
    parents = serializers.SerializerMethodField(read_only=True)
    parent_public_ids = serializers.SlugRelatedField(
        queryset=BimaErpSaleDocument.objects.all(),
        slug_field='public_id',
        source='parents',
        write_only=True,
        many=True,
        required=False,  # this allows the field to be empty
    )

    # other fields ...

    def get_parents(self, obj):
        return [
            {
                'id': parent.public_id.hex,
                'numbers': parent.numbers,
            }
            for parent in obj.parents.all()
        ]

    class Meta:
        model = BimaErpSaleDocument
        fields = [
            'id', 'numbers', 'date', 'status', 'type', 'partner', 'partner_public_id', 'note',
            'private_note', 'validity', 'payment_terms', 'delivery_terms', 'subtotal', 'taxes',
            'discounts', 'total', 'parents', 'parent_public_ids', 'history', 'created', 'updated'
        ]
        read_only_fields = ('history',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        request = self.context.get('request')
        if request and request.path.endswith(instance.public_id.hex):
            history = SaleDocumentHistorySerializer(instance.history.all(), many=True).data
            representation['history'] = history

        return representation


class SaleDocumentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BimaErpSaleDocument.history.model
        fields = ['id', 'numbers', 'date', 'status', 'type', 'partner_public_id',
                  'note', 'private_note', 'validity', 'payment_terms', 'delivery_terms',
                  'subtotal', 'taxes', 'discounts', 'total', 'parent_public_id', 'history_type',
                  'history_date', 'history_user']


class SaleDocumentProductSerializer(serializers.Serializer):
    product_public_id = serializers.UUIDField()
    quantity = serializers.DecimalField(max_digits=18, decimal_places=3)
    unit_price = serializers.DecimalField(max_digits=18, decimal_places=3)
    vat = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    description = serializers.CharField(max_length=500, required=False)
    discount = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)

    def create(self, validated_data):
        product = BimaErpProduct.objects.get(public_id=validated_data['product_public_id'])
        sale_document = BimaErpSaleDocument.objects.get(public_id=self.context['sale_document_public_id'])
        sale_document_product = BimaErpSaleDocumentProduct.objects.create(
            sale_document=sale_document,
            product=product,
            **validated_data
        )
        return sale_document_product

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.unit_price = validated_data.get('unit_price', instance.unit_price)
        instance.vat = validated_data.get('vat', instance.vat)
        instance.description = validated_data.get('description', instance.description)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.save()
        return instance
