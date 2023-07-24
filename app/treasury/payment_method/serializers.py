from .models import BimaTreasuryPaymentMethod
from core.abstract.serializers import AbstractSerializer


class BimaTreasuryPaymentMethosdSerializer(AbstractSerializer):
    class Meta:
        model = BimaTreasuryPaymentMethod
        fields = '__all__'
