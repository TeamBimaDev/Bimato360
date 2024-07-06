from core.abstract.serializers import AbstractSerializer
from .models import BimaHrActivityType

class BimaHrActivityTypeSerializer(AbstractSerializer):
    class Meta:
        model = BimaHrActivityType
        fields = '__all__'
