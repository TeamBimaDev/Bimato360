from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from core.abstract.serializers import AbstractSerializer

from erp.product.models import BimaErpProduct
from .models import BimaErpPurchaseDocument, BimaErpPurchaseDocumentProduct
from ..partner.models import BimaErpPartner
from django.utils.translation import gettext_lazy as _


class BimaErpPurchaseDocumentSerializer(AbstractSerializer):
    history = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField(read_only=True)

    # Other methods ...

    parents = serializers.SerializerMethodField(read_only=True)
    parent_public_ids = serializers.SlugRelatedField(
        queryset=BimaErpPurchaseDocument.objects.all(),
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
        serializer = BimaErpPurchaseDocumentHistorySerializer(history_instances, many=True)
        return serializer.data

    def get_children(self, obj):
        return [
            {
                'id': child.public_id.hex,
                'number': child.number,
            }
            for child in obj.bimaerppurchasedocument_set.all()
        ] if obj.bimaerppurchasedocument_set else []

    class Meta:
        model = BimaErpPurchaseDocument
        fields = [
            'id', 'number', 'date', 'status', 'type', 'partner', 'partner_public_id', 'note',
            'private_note', 'validity', 'payment_terms', 'delivery_terms', 'total_vat', 'total_amount',
            'total_discount', 'parents', 'parent_public_ids', 'history', 'vat_label', 'vat_amount', 'created',
            'updated', 'total_vat', 'total_amount', 'total_discount', 'children'
        ]
        read_only_fields = ('total_vat', 'total_amount', 'total_discount',)


class BimaErpPurchaseDocumentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BimaErpPurchaseDocument.history.model
        fields = ['id', 'number', 'date', 'status', 'type', 'partner_id',
                  'note', 'private_note', 'validity', 'payment_terms', 'delivery_terms', 'vat_label', 'vat_amount',
                  'total_amount', 'total_discount', 'total_vat', 'history_type', 'history_date',
                  'history_user']


class BimaErpPurchaseDocumentProductSerializer(serializers.Serializer):
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
    unit_of_measure = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(max_length=500, required=False, allow_blank=True)
    discount = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    total_without_vat = serializers.DecimalField(max_digits=18, decimal_places=3, required=False)
    total_after_discount = serializers.DecimalField(max_digits=18, decimal_places=3, required=False)
    total_price = serializers.DecimalField(max_digits=18, decimal_places=3, required=False)
    discount_amount = serializers.DecimalField(max_digits=18, decimal_places=3, required=False)
    vat_amount = serializers.DecimalField(max_digits=18, decimal_places=3, required=False)

    class Meta:
        model = BimaErpPurchaseDocumentProduct
        fields = ['product', 'product_public_id', 'name', 'reference', 'quantity', 'unit_price', 'vat', 'description',
                  'discount', 'total_without_vat', 'total_after_discount', 'total_price', 'discount_amount',
                  'vat_amount', 'unit_of_measure']

        read_only_fields = ('total_without_vat', 'total_after_discount', 'total_price', 'discount_amount', 'vat_amount')

    def validate(self, attrs):
        product = attrs['product']
        purchase_document = self.context.get('purchase_document')
        if BimaErpPurchaseDocumentProduct.objects.filter(purchase_document=purchase_document, product=product).exists():
            raise serializers.ValidationError("This product already exists in the document.")
        return attrs

    def validate_quantity(self, desired_quantity):

        if self.instance:
            product = self.instance.product
        else:
            try:
                product_public_id = self.initial_data.get('product_public_id', '')
                product = BimaErpProduct.objects.get(public_id=product_public_id)
            except ObjectDoesNotExist:
                raise serializers.ValidationError(_("No product with this id exists."))

        net_change_in_quantity = desired_quantity
        if not BimaErpPurchaseDocumentProduct.is_quantity_available(product, net_change_in_quantity):
            raise serializers.ValidationError(_("Not enough stock available for this product."))
        return desired_quantity

    def validate_product_public_id(self, value):
        if not BimaErpProduct.objects.filter(public_id=str(value.public_id)).exists():
            raise serializers.ValidationError(_("No product with this id exists."))
        return value

    def create(self, validated_data):
        product = validated_data.pop('product')
        purchase_document = self.context.pop('purchase_document')
        purchase_document_product = BimaErpPurchaseDocumentProduct.objects.create(
            purchase_document=purchase_document,
            product=product,
            **validated_data
        )
        return purchase_document_product

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.unit_price = validated_data.get('unit_price', instance.unit_price)
        instance.vat = validated_data.get('vat', instance.vat)
        instance.description = validated_data.get('description', instance.description)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.name = validated_data.get('name', instance.name)
        instance.unit_of_measure = validated_data.get('unit_of_measure', instance.unit_of_measure)
        instance.save()
        return instance


class BimaErpPurchaseDocumentProductHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BimaErpPurchaseDocumentProduct.history.model
        fields = [
            'id', 'purchase_document_public_id', 'name', 'reference', 'quantity', 'unit_price', 'vat', 'vat_amount',
            'description', 'discount', 'discount_amount', 'total_without_vat',
            'total_after_discount', 'total_price', 'history_type', 'history_date'
        ]