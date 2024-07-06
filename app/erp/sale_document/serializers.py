from core.abstract.serializers import AbstractSerializer
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from erp.partner.models import BimaErpPartner
from erp.product.models import BimaErpProduct
from rest_framework import serializers
from treasury.payment_term.models import BimaTreasuryPaymentTerm
from treasury.transaction.serializers_helper import SimpleTransactionSaleDocumentPaymentSerializer

from .models import BimaErpSaleDocument, BimaErpSaleDocumentProduct


class BimaErpSaleDocumentSerializer(AbstractSerializer):
    history = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField(read_only=True)
    recurring_stopped_by_display = serializers.SerializerMethodField(read_only=True)
    recurring_reactivated_by_display = serializers.SerializerMethodField(read_only=True)

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
                'is_recurring': parent.is_recurring,
                'is_recurring_parent': parent.is_recurring_parent,
                'recurring_initial_parent_public_id': parent.recurring_initial_parent_public_id,
            }
            for parent in obj.parents.all()
        ] if obj.parents else []

    def get_history(self, obj):
        history_instances = list(obj.history.all())
        serializer = BimaErpSaleDocumentHistorySerializer(history_instances, many=True)
        return serializer.data

    def get_children(self, obj):
        return [
            {
                'id': child.public_id.hex,
                'number': child.number,
            }
            for child in obj.bimaerpsaledocument_set.all()
        ] if obj.bimaerpsaledocument_set else []

    def get_recurring_stopped_by_display(self, obj):
        if obj.recurring_stopped_by:
            return {
                'name': obj.recurring_stopped_by.name,
                "public_id": obj.recurring_stopped_by.public_id
            }
        return None

    def get_recurring_reactivated_by_display(self, obj):
        if obj.recurring_reactivated_by:
            return {
                'name': obj.recurring_reactivated_by.name,
                'public_id': obj.recurring_reactivated_by.public_id
            }
        return None

    def get_payment_terms(self, obj):
        if obj.payment_terms:
            return {
                'id': obj.payment_terms.public_id.hex,
                'name': obj.payment_terms.name,
            }
        return None

    class Meta:
        model = BimaErpSaleDocument

        fields = [
            'id', 'number', 'date', 'status', 'type', 'partner', 'partner_public_id', 'note',
            'private_note', 'validity', 'payment_terms', 'payment_terms_public_id', 'delivery_terms', 'total_vat',
            'total_discount', 'parents', 'parent_public_ids', 'history', 'vat_label', 'vat_amount', 'created',
            'updated', 'total_vat', 'total_amount', 'total_discount', 'children', 'is_recurring', 'is_recurring_parent',
            'recurring_initial_parent_id', 'recurring_initial_parent_public_id', 'recurring_interval',
            'recurring_interval_type_custom_number', 'recurring_interval_type_custom_unit', 'recurring_cycle',
            'recurring_cycle_number_to_repeat', 'recurring_cycle_stop_at', 'recurring_cycle_stopped_at',
            'recurring_last_generated_day', 'recurring_reason_stop', 'recurring_reason_reactivated',
            'recurring_reactivated_date', 'recurring_stopped_by_display', 'recurring_reactivated_by_display',
            'is_recurring_ended', 'payment_status', 'amount_paid', 'is_payment_late', 'next_due_date', 'days_in_late',
            'last_generated_file_url'
        ]
        read_only_fields = (
            'total_vat', 'total_amount', 'total_discount', 'amount_paid', 'is_payment_late', 'next_due_date',
            'days_in_late', 'last_generated_file_url')


class BimaErpSaleDocumentUnpaidSerializer(AbstractSerializer):
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
        TransactionSaleDocumentPayment = apps.get_model('treasury', 'TransactionSaleDocumentPayment')
        transactions = TransactionSaleDocumentPayment.objects.filter(sale_document=obj)
        return SimpleTransactionSaleDocumentPaymentSerializer(transactions, many=True).data

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
        model = BimaErpSaleDocument

        fields = [
            'id', 'number', 'date', 'status', 'type', 'partner', 'partner_public_id', 'note',
            'private_note', 'validity', 'payment_terms', 'payment_terms_public_id', 'total_vat',
            'total_discount', 'vat_amount', 'total_vat', 'total_amount', 'total_discount', 'payment_status',
            'amount_paid', 'transactions', 'last_generated_file_url'
        ]
        read_only_fields = (
        'total_vat', 'total_amount', 'total_discount', 'amount_paid', 'transactions', 'last_generated_file_url')


class BimaErpSaleDocumentHistorySerializer(serializers.ModelSerializer):
    recurring_stopped_by_display = serializers.SerializerMethodField(read_only=True)
    recurring_reactivated_by_display = serializers.SerializerMethodField(read_only=True)

    history_user_display = serializers.SerializerMethodField(read_only=True)

    def get_recurring_stopped_by_display(self, obj):
        if obj.recurring_stopped_by:
            return obj.recurring_stopped_by.name
        return None

    def get_recurring_reactivated_by_display(self, obj):
        if obj.recurring_reactivated_by:
            return obj.recurring_reactivated_by.name
        return None

    def get_history_user_display(self, obj):
        if obj.history_user:
            return obj.history_user.name
        return None

    class Meta:
        model = BimaErpSaleDocument.history.model
        fields = ['id', 'number', 'date', 'status', 'type', 'partner_id',
                  'note', 'private_note', 'validity', 'payment_terms', 'delivery_terms', 'vat_label', 'vat_amount',
                  'total_amount', 'total_discount', 'total_vat', 'history_type', 'history_date', 'is_recurring',
                  'is_recurring_parent', 'recurring_initial_parent_id', 'recurring_initial_parent_public_id',
                  'recurring_interval', 'recurring_interval_type_custom_number', 'recurring_interval_type_custom_unit',
                  'recurring_cycle', 'recurring_cycle_number_to_repeat', 'recurring_cycle_stop_at',
                  'recurring_cycle_stopped_at', 'recurring_last_generated_day', 'recurring_reason_stop',
                  'recurring_reason_reactivated', 'recurring_reactivated_date', 'history_user_display',
                  'recurring_stopped_by_display', 'recurring_reactivated_by_display', 'is_recurring_ended',
                  'payment_status', 'amount_paid', 'is_payment_late', 'next_due_date', 'days_in_late',
                  'last_generated_file_url']


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
    unit_of_measure = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(max_length=500, required=False, allow_blank=True)
    discount = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    total_without_vat = serializers.DecimalField(max_digits=18, decimal_places=3, required=False)
    total_after_discount = serializers.DecimalField(max_digits=18, decimal_places=3, required=False)
    total_price = serializers.DecimalField(max_digits=18, decimal_places=3, required=False)
    discount_amount = serializers.DecimalField(max_digits=18, decimal_places=3, required=False)
    vat_amount = serializers.DecimalField(max_digits=18, decimal_places=3, required=False)

    class Meta:
        model = BimaErpSaleDocumentProduct
        fields = ['product', 'product_public_id', 'name', 'reference', 'quantity', 'unit_price', 'vat', 'description',
                  'discount', 'total_without_vat', 'total_after_discount', 'total_price', 'discount_amount',
                  'vat_amount', 'unit_of_measure']

        read_only_fields = ('total_without_vat', 'total_after_discount', 'total_price', 'discount_amount', 'vat_amount')

    def validate(self, attrs):
        product = attrs['product']
        sale_document = self.context.get('sale_document')
        if BimaErpSaleDocumentProduct.objects.filter(sale_document=sale_document, product=product).exists():
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
        if not BimaErpSaleDocumentProduct.is_quantity_available(product, net_change_in_quantity):
            raise serializers.ValidationError(_("Not enough stock available for this product."))
        return desired_quantity

    def validate_product_public_id(self, value):
        if not BimaErpProduct.objects.filter(public_id=str(value.public_id)).exists():
            raise serializers.ValidationError(_("No product with this id exists."))
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
        instance.name = validated_data.get('name', instance.name)
        instance.unit_of_measure = validated_data.get('unit_of_measure', instance.unit_of_measure)
        instance.save()
        return instance


class BimaErpSaleDocumentProductHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BimaErpSaleDocumentProduct.history.model
        fields = [
            'id', 'sale_document_public_id', 'name', 'reference', 'quantity', 'unit_price', 'vat', 'vat_amount',
            'description', 'discount', 'discount_amount', 'total_without_vat', 'unit_of_measure',
            'total_after_discount', 'total_price', 'history_type', 'history_date'
        ]
