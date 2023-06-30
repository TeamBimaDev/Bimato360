from .models import BimaCoreTag
from core.abstract.serializers import AbstractSerializer
from rest_framework import serializers


class BimaCoreTagSerializer(AbstractSerializer):
    parent = serializers.SerializerMethodField(read_only=True)
    parent_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreTag.objects.all(),
        slug_field='public_id',
        source='parent',
        write_only=True,
        required=False
    )

    def get_parent(self, obj):
        if obj.parent:
            return {
                'id': obj.parent.public_id.hex,
                'name': obj.parent.name,
            }
        return None

    class Meta:
        model = BimaCoreTag
        fields = ['id', 'name', 'public_id', 'parent', 'parent_public_id']
