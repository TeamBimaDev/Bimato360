import logging

from common.enums.transaction_enum import PaymentTermType, get_payment_term_custom_type
from core.abstract.serializers import AbstractSerializer
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import BimaTreasuryPaymentTerm, BimaTreasuryPaymentTermDetail

logger = logging.getLogger(__name__)


class BimaTreasuryPaymentTermDetailSerializer(AbstractSerializer):
    payment_term = serializers.SerializerMethodField(read_only=True)
    payment_term_public_id = serializers.SlugRelatedField(
        queryset=BimaTreasuryPaymentTerm.objects.all(),
        slug_field='public_id',
        source='payment_term',
        write_only=True,
        required=False
    )

    def get_payment_term(self, obj):
        return {
            'id': obj.payment_term.public_id.hex,
            'name': obj.payment_term.name,
        }

    class Meta:
        model = BimaTreasuryPaymentTermDetail
        fields = [
            'id', 'percentage', 'value', 'payment_term', 'payment_term_public_id', 'created', 'updated'
        ]


class BimaTreasuryPaymentTermSerializer(AbstractSerializer):
    payment_term_details = BimaTreasuryPaymentTermDetailSerializer(many=True, required=False)

    class Meta:
        model = BimaTreasuryPaymentTerm
        fields = [
            'id', 'name', 'active', 'note', 'code', 'type', 'is_system', 'payment_term_details', 'created', 'updated'
        ]
        depth = 1
        read_only_fields = ('code', 'is_system',)

    def validate_payment_term_details(self, payment_term_details):
        total_percent = sum(
            line['percentage'] for line in payment_term_details)
        if total_percent != 100:
            raise serializers.ValidationError({str(_("Payment terms details")): _("Total percentage must be 100%.")})
        return payment_term_details

    def validate_value(self, value):
        valid_choices = [choice[0] for choice in get_payment_term_custom_type()]
        if value not in valid_choices:
            raise serializers.ValidationError(
                _("Invalid value for payment term detail. value: %(value)") % {
                    'value': value}
            )
        return value

    def validate(self, data):
        payment_term_type = data.get('type')
        if payment_term_type == PaymentTermType.CUSTOM.name:
            payment_term_details = data.get('payment_term_details', [])
            self.validate_payment_term_details(payment_term_details)
        return data

    def create(self, validated_data):
        payment_term_details = validated_data.pop('payment_term_details', [])
        with transaction.atomic():
            try:
                payment_term = BimaTreasuryPaymentTerm.objects.create(**validated_data)

                if validated_data.get('type') == PaymentTermType.CUSTOM.name:
                    for line_data in payment_term_details:
                        self.validate_value(line_data['value'])
                        BimaTreasuryPaymentTermDetail.objects.create(payment_term=payment_term, **line_data)

                return payment_term

            except Exception as e:
                logger.error(f"Error while creating BimaTreasuryPaymentTerm: {e}")
                raise

    def update(self, instance, validated_data):
        payment_term_details = validated_data.pop('payment_term_details', [])
        with transaction.atomic():
            try:
                instance.name = validated_data.get('name', instance.name)
                instance.active = validated_data.get('active', instance.active)
                instance.note = validated_data.get('note', instance.note)
                instance.type = validated_data.get('type', instance.type)
                instance.save()

                if validated_data.get('type') == PaymentTermType.CUSTOM.name:
                    instance.payment_term_details.all().delete()
                    for line_data in payment_term_details:
                        self.validate_value(line_data['value'])
                        BimaTreasuryPaymentTermDetail.objects.create(payment_term=instance, **line_data)

                else:
                    instance.payment_term_details.all().delete()

                return instance

            except Exception as e:
                logger.error(f"Error while updating BimaTreasuryPaymentTerm {instance.public_id} : {e}")
                raise
