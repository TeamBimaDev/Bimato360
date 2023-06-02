from core.entity_tag.models import BimaCoreEntityTag
from core.abstract.serializers import AbstractSerializer
from rest_framework import serializers

from core.tag.models import BimaCoreTag


class BimaCoreEntityTagSerializer(AbstractSerializer):
    tag = serializers.SerializerMethodField(read_only=True)
    tag_id = serializers.PrimaryKeyRelatedField(
        queryset=BimaCoreTag.objects.all(),
        source='tag',
        write_only=True
    )

    def get_tag(self, obj):
        return {
            'id': obj.tag.public_id.hex,
            'name': obj.tag.name,
        }

    class Meta:
        model = BimaCoreEntityTag
        fields = 'id', 'id_manager', 'tag', 'tag_id', 'created', 'updated'
