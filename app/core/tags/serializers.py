from core.tags.models import BimaCoreTags
from core.abstract.serializers import AbstractSerializer
class BimaCoreTagsserializer(AbstractSerializer):
    class Meta:
        model = BimaCoreTags
        fields = '__all__'
