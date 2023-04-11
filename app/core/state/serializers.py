from core.abstract.serializers import AbstractSerializer
from core.state.models import BimaCoreState


class BimaCoreStateSerializer(AbstractSerializer):
    class Meta:
        model = BimaCoreState
        fields = ['id', 'name', 'code', 'country', 'created', 'updated']

