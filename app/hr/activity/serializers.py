from core.abstract.serializers import AbstractSerializer
from .models import BimaHrActivity

class BimaHrActivitySerializer(AbstractSerializer):
    class Meta:
        model = BimaHrActivity
        fields = '__all__'
