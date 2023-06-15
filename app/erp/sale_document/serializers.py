from rest_framework import serializers

from core.abstract.serializers import AbstractSerializer

from erp.product.models import BimaErpProduct
from .models import BimaErpSaleDocument, BimaErpSaleDocumentProduct
from ..partner.models import BimaErpPartner


class BimaErpSaleDocumentSerializer(AbstractSerializer):
    history = serializers.SerializerMethodField()

    parents = serializers.SerializerMethodField(read_only=True)
    parent_public_ids = serializers.SlugRelatedField(
        queryset=BimaErpSaleDocument.objects.all(),
        slug_field='public_id',
        source='parents',
        write_only=True,
        many=True,
        required=False,
    )

    partner = serializers.SerializerMethodField(read_only=True)
    partner_public_id = serializers.SlugRelatedField(
        queryset=BimaErpPartner.objects.all(),
        slug_field='public_id',
        source='partner',
        write_only=True
    )

    def get_partner(self, obj):
        return {
            'id': obj.partner.public_id.hex,
            'partner_type': obj.partner.partner_type,
            'first_name': obj.partner.first_name,
            'last_name': obj.partner.last_name,
            'company_name': obj.partner.company_name,
        }

    def get_parents(self, obj):
        return [
            {
                'id': parent.public_id.hex,
                'number': parent.number,
            }
            for parent in obj.parents.all()
        ] if obj.parents else []

    def get_history(self, obj):
        history_instances = list(obj.history.all())
        serializer = BimaErpSaleDocumentHistorySerializer(history_instances, many=True)
        return serializer.data

    class Meta:
        model = BimaErpSaleDocument
        fields = [
            'id', 'number', 'date', 'status', 'type', 'partner', 'partner_public_id', 'note',
            'private_note', 'validity', 'payment_terms', 'delivery_terms', 'total_vat', 'total_amount',
            'total_discount', 'parents', 'parent_public_ids', 'history', 'vat_label', 'vat_amount', 'created', 'updated'
        ]
        read_only_fields = ('total_vat', 'total_amount', 'total_discount',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        request = self.context.get('request')
        if request and request.path.endswith(instance.public_id.hex):
            history = self.get_history(instance)
            representation['history'] = history

        return representation


class BimaErpSaleDocumentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BimaErpSaleDocument.history.model
        fields = ['id', 'number', 'date', 'status', 'type', 'partner_id',
                  'note', 'private_note', 'validity', 'payment_terms', 'delivery_terms', 'vat_label', 'vat_amount'
                  'total_amount', 'total_discount', 'total_vat', 'history_type', 'history_date',
                  'history_user']


class BimaErpSaleDocumentProductSerializer(serializers.Serializer):
    product_public_id = serializers.SlugRelatedField(
        queryset=BimaErpProduct.objects.all(),
        slug_field='public_id',
        source='product',
        write_only=True
    )
    product = serializers.SerializerMethodField()

    def get_product(self, obj):
        return obj.product.public_id

    name = serializers.CharField(max_length=255, required=True)
    reference = serializers.CharField(max_length=255, required=True)
    quantity = serializers.DecimalField(max_digits=18, decimal_places=3)
    unit_price = serializers.DecimalField(max_digits=18, decimal_places=3)
    vat = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    description = serializers.CharField(max_length=500, required=False)
    discount = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)

    class Meta:
        model = BimaErpSaleDocumentProduct
        fields = ['product', 'product_public_id', 'name', 'reference', 'quantity', 'unit_price', 'vat', 'description',
                  'discount']
        read_only_fields = ('total_without_vat', 'total_after_discount', 'total_price',)


    def validate(self, attrs):
        product = attrs['product']
        sale_document = self.context.get('sale_document')
        if BimaErpSaleDocumentProduct.objects.filter(sale_document=sale_document, product=product).exists():
            raise serializers.ValidationError("This product already exists in the document.")
        return attrs

    def validate_product_public_id(self, value):
        if not BimaErpProduct.objects.filter(public_id=str(value.public_id)).exists():
            raise serializers.ValidationError("No product with this id exists.")
        return value

    def create(self, validated_data):
        product = validated_data.pop('product')
        sale_document = self.context.pop('sale_document')
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


class BimaErpSaleDocumentProductHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BimaErpSaleDocumentProduct.history.model
        fields = [
            'id', 'sale_document_public_id', 'name', 'reference', 'quantity', 'unit_price', 'vat', 'vat_amount',
            'description', 'discount', 'discount_amount', 'total_without_vat',
            'total_after_discount', 'total_price', 'history_type', 'history_date'
        ]
