from core.abstract.serializers import AbstractSerializer
from hr.refuse.models import BimaHrRefuse

class BimaHrRefuseSerializer(AbstractSerializer):
    class Meta:
        model = BimaHrRefuse
        fields = '__all__'
