from core.abstract.serializers import AbstractSerializer
from .models import BimaHrCondidatPoste

class BimaHrCondidatPosteSerializer(AbstractSerializer):
    class Meta:
        model = BimaHrCondidatPoste
        fields = '__all__'
