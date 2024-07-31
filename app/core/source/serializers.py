<<<<<<< HEAD
from core.abstract.serializers import AbstractSerializer
from core.source.models import BimaCoreSource


class BimaCoreSourceSerializer(AbstractSerializer):
    class Meta:
        model = BimaCoreSource
        fields = ['id', 'name', 'description', 'active', 'public_id', 'created', 'updated']
=======
from core.abstract.serializers import AbstractSerializer
from core.source.models import BimaCoreSource


class BimaCoreSourceSerializer(AbstractSerializer):
    class Meta:
        model = BimaCoreSource
        fields = ['id', 'name', 'description', 'active', 'public_id', 'created', 'updated']
>>>>>>> origin/ma-branch
