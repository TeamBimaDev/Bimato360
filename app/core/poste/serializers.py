from core.abstract.serializers import AbstractSerializer
from .models import BimaCorePoste

class BimaCorePostESerializer(AbstractSerializer):
    class Meta:
        model = BimaCorePoste
        fields = '__all__'