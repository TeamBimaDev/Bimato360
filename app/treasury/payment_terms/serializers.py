from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import BimaTreasuryPaymentTerms
from core.abstract.serializers import AbstractSerializer
from treasury.payment_terms_details.models import BimaTreasuryPaymentTermsDetails
from treasury.payment_terms_details.serializers import BimaTreasuryPaymentTermsDetailsSerializer


class BimaTreasuryPaymentTermsSerializer(AbstractSerializer):
    payment_terms_details = BimaTreasuryPaymentTermsDetailsSerializer(many=True, required=False, write_only=True)

    class Meta:
        model = BimaTreasuryPaymentTerms
        fields = '__all__'

    def validate_payment_terms_details(self, payment_terms_details):
        total_value = sum(detail.get('value', 0) for detail in payment_terms_details)
        if total_value != 100:
            raise serializers.ValidationError(_("Sum of payment_terms_details value must be 100."))
        return payment_terms_details

    def create(self, validated_data):
        payment_terms_details = validated_data.pop('payment_terms_details', [])

        payment_terms = BimaTreasuryPaymentTerms.objects.create(**validated_data)

        for detail in payment_terms_details:
            BimaTreasuryPaymentTermsDetails.objects.create(payment_terms=payment_terms, **detail)

        return payment_terms

    def update(self, instance, validated_data):
        payment_terms_details = validated_data.pop('payment_terms_details', None)

        # Update payment_terms instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or create associated payment_terms_details
        if payment_terms_details is not None:
            # Delete old payment_terms_details
            instance.payment_terms_details.all().delete()

            # Recreate new payment_terms_details
            for detail in payment_terms_details:
                BimaTreasuryPaymentTermsDetails.objects.create(payment_terms=instance, **detail)
