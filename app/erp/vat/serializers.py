from .models import BimaErpVat
from core.abstract.serializers import AbstractSerializer


class BimaErpVatSerializer(AbstractSerializer):
    class Meta:
        model = BimaErpVat
        fields = '__all__'
