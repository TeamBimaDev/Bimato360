from core.abstract.serializers import AbstractSerializer
from django.apps import apps
from django.utils.translation import gettext_lazy as _
from erp.partner.models import BimaErpPartner
from erp.product.models import BimaErpProduct
from rest_framework import serializers
from treasury.payment_term.models import BimaTreasuryPaymentTerm
from treasury.transaction.serializers_helper import SimpleTransactionPurchaseDocumentPaymentSerializer

from .models import BimaErpPurchaseDocument, BimaErpPurchaseDocumentProduct


class BimaErpPurchaseDocumentSerializer(AbstractSerializer):
    history = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField(read_only=True)

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

    payment_terms = serializers.SerializerMethodField(read_only=True)
    payment_terms_public_id = serializers.SlugRelatedField(
        queryset=BimaTreasuryPaymentTerm.objects.all(),
        slug_field='public_id',
        source='payment_terms',
        write_only=True,
        required=False,
        allow_null=True,
        allow_empty=True
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

    def get_payment_terms(self, obj):
        if obj.payment_terms:
            return {
                'id': obj.payment_terms.public_id.hex,
                'name': obj.payment_terms.name,
            }
        return None

    class Meta:
        model = BimaErpPurchaseDocument
        fields = [
            'id', 'number', 'number_at_partner', 'date', 'status', 'type', 'partner', 'partner_public_id', 'vat_label',
            'vat_amount', 'note', 'private_note', 'validity', 'payment_terms', 'payment_terms_public_id',
            'delivery_terms', 'total_amount_without_vat', 'total_after_discount', 'total_vat', 'total_amount',
            'total_discount', 'parents', 'parent_public_ids', 'history', 'created', 'updated', 'children',
            'payment_status', 'amount_paid'
        ]
        read_only_fields = ('total_vat', 'total_amount', 'total_discount', 'amount_paid',)


class BimaErpPurchaseDocumentHistorySerializer(serializers.ModelSerializer):
    history_user_display = serializers.SerializerMethodField(read_only=True)

    def get_history_user_display(self, obj):
        if obj.history_user:
            return obj.history_user.name
        return None

    class Meta:
        model = BimaErpPurchaseDocument.history.model
        fields = ['id', 'number', 'number_at_partner', 'date', 'status', 'type', 'partner_id',
                  'note', 'private_note', 'validity', 'payment_terms', 'delivery_terms', 'vat_label', 'vat_amount',
                  'total_amount', 'total_discount', 'total_vat', 'history_type', 'history_date', 'history_user_display']


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


class BimaErpPurchaseDocumentUnpaidSerializer(AbstractSerializer):
    partner = serializers.SerializerMethodField(read_only=True)
    partner_public_id = serializers.SlugRelatedField(
        queryset=BimaErpPartner.objects.all(),
        slug_field='public_id',
        source='partner',
        write_only=True
    )

    payment_terms = serializers.SerializerMethodField(read_only=True)
    payment_terms_public_id = serializers.SlugRelatedField(
        queryset=BimaTreasuryPaymentTerm.objects.all(),
        slug_field='public_id',
        source='payment_terms',
        write_only=True,
        required=False,
        allow_null=True,
        allow_empty=True
    )

    transactions = serializers.SerializerMethodField()

    def get_transactions(self, obj):
        TransactionPurchaseDocumentPayment = apps.get_model('treasury', 'TransactionPurchaseDocumentPayment')
        transactions = TransactionPurchaseDocumentPayment.objects.filter(purchase_document=obj)
        return SimpleTransactionPurchaseDocumentPaymentSerializer(transactions, many=True).data

    def get_partner(self, obj):
        return {
            'id': obj.partner.public_id.hex,
            'partner_type': obj.partner.partner_type,
            'first_name': obj.partner.first_name,
            'last_name': obj.partner.last_name,
            'company_name': obj.partner.company_name,
        }

    def get_payment_terms(self, obj):
        if obj.payment_terms:
            return {
                'id': obj.payment_terms.public_id.hex,
                'name': obj.payment_terms.name,
            }
        return None

    class Meta:
        model = BimaErpPurchaseDocument

        fields = [
            'id', 'number', 'date', 'status', 'type', 'partner', 'partner_public_id', 'note',
            'private_note', 'validity', 'total_vat', 'total_discount', 'vat_amount', 'total_vat', 'total_amount',
            'total_discount', 'payment_status', 'amount_paid', 'transactions', 'payment_terms',
            'payment_terms_public_id',
        ]
        read_only_fields = ('total_vat', 'total_amount', 'total_discount', 'amount_paid', 'transactions')
