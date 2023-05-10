from core.abstract.serializers import AbstractSerializer
from .models import BimaPartnersPayment

class BimaPartnersPaymentSerializer(AbstractSerializer):
    class Meta:
        model = BimaPartnersPayment
        fields = '__all__'
