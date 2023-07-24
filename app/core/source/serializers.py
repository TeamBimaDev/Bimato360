from core.abstract.serializers import AbstractSerializer
from core.source.models import BimaCoreSource


class BimaCoreSourceSerializer(AbstractSerializer):
    class Meta:
        model = BimaCoreSource
        fields = '__all__'
