
from core.abstract.serializers import AbstractSerializer

from core.document.models import BimaCoreDocument


class BimaCoreDocumentSerializer(AbstractSerializer):
    class Meta:
        model = BimaCoreDocument
        fields = '__all__'


class BimaCoreDocumentGetSerializer(AbstractSerializer):
    class Meta:
        model = BimaCoreDocument
        fields = ['public_id', 'document_name', 'description', 'date_file', 'file_type','file_path']
