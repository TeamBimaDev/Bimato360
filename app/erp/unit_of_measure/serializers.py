

from .models import BimaErpUnitOfMeasure
from core.abstract.serializers import AbstractSerializer


class BimaErpUnitOfMeasureSerializer(AbstractSerializer):
    class Meta:
        model = BimaErpUnitOfMeasure
        fields = '__all__'


