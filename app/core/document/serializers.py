from core.abstract.serializers import AbstractSerializer

from core.document.models import BimaCoreDocument


class BimaCoreDocumentSerializer(AbstractSerializer):
    class Meta:
        model = BimaCoreDocument
        fields = '__all__'
