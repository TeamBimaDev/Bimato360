from core.abstract.serializers import AbstractSerializer
from .models import BimaCorePost

class BimaCorePostSerializer(AbstractSerializer):
    class Meta:
        model = BimaCorePost
        fields = '__all__'