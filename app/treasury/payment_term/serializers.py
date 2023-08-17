from common.enums.transaction_enum import PaymentTermDetailType
from core.abstract.serializers import AbstractSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import BimaTreasuryPaymentTerm
from ..payment_term_detail.models import BimaTreasuryPaymentTermDetail
from ..payment_term_detail.serializers import BimaTreasuryPaymentTermDetailSerializer


class BimaTreasuryPaymentTermSerializer(AbstractSerializer):
    payment_term_details = BimaTreasuryPaymentTermDetailSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = BimaTreasuryPaymentTerm
        fields = [
            'id', 'name', 'active', 'note', 'code', 'is_system', 'payment_term_details', 'created', 'updated'
        ]
        depth = 1

    def create(self, validated_data):
        payment_term_details = validated_data.pop('payment_term_details')
        payment_term = BimaTreasuryPaymentTerm.objects.create(**validated_data)
        for line_data in payment_term_details:
            BimaTreasuryPaymentTermDetail.objects.create(payment_term=payment_term, **line_data)
        return payment_term

    def update(self, instance, validated_data):
        payment_term_details = validated_data.pop('payment_term_details')
        instance.name = validated_data.get('name', instance.name)
        instance.active = validated_data.get('active', instance.active)
        instance.note = validated_data.get('note', instance.note)
        instance.save()

        for line_data in payment_term_details:
            BimaTreasuryPaymentTermDetail.objects.update_or_create(payment_term=instance, **line_data)

        return instance

    def validate(self, data):
        payment_term_details = data.get('payment_term_details', [])

        total_percent = sum(
            line['value'] for line in payment_term_details if line['type'] == PaymentTermDetailType.PERCENT.name)
        if any(line['type'] == 'percent' for line in payment_term_details) and total_percent != 100:
            raise serializers.ValidationError({"lines": _("Total percentage of percentage-type lines must be 100%.")})

        return data
