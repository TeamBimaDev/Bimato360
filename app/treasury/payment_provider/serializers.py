from .models import BimaTreasuryPaymentProvider
from core.abstract.serializers import AbstractSerializer


class BimaTreasuryPaymentProviderSerializer(AbstractSerializer):
    class Meta:
        model = BimaTreasuryPaymentProvider
        fields = '__all__'
