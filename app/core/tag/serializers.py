from core.tag.models import BimaCoreTag
from core.abstract.serializers import AbstractSerializer


class BimaCoreTagSerializer(AbstractSerializer):
    class Meta:
        model = BimaCoreTag
        fields = '__all__'
