from core.entity_tag.models import BimaCoreEntityTag
from core.abstract.serializers import AbstractSerializer


class BimaCoreEntityTagSerializer(AbstractSerializer):
    class Meta:
        model = BimaCoreEntityTag
        fields = '__all__'
