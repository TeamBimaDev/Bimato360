from .models import BimaCoreTag
from core.abstract.serializers import AbstractSerializer
from rest_framework import serializers
import re
import random
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _


class BimaCoreTagSerializer(AbstractSerializer):
    parent = serializers.SerializerMethodField(read_only=True)
    parent_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreTag.objects.all(),
        slug_field='public_id',
        source='parent',
        write_only=True,
        required=False,
        allow_null=True,
        allow_empty=True
    )
    direct_children_count = serializers.SerializerMethodField()

    class Meta:
        model = BimaCoreTag
        fields = ['id', 'name', 'public_id', 'parent', 'parent_public_id', 'color', 'direct_children_count']

    def get_parent(self, obj):
        if obj.parent:
            return {
                'id': obj.parent.public_id.hex,
                'name': obj.parent.name,
            }
        return None

    def validate_color(self, value):
        if value and not re.match('^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', value):
            raise serializers.ValidationError(_("This field should be a valid hex color."))
        return value

    def to_internal_value(self, data):
        if 'parent_public_id' in data and data['parent_public_id'] == "":
            data['parent_public_id'] = None
        return super().to_internal_value(data)

    def validate_parent_public_id(self, value):
        if not value:
            return value

        tag_to_edit = self.instance
        proposed_parent = value

        if proposed_parent and self.instance:
            if self.is_descendant(tag_to_edit, proposed_parent):
                raise serializers.ValidationError({"Tag parent":
                                                       _("A tag cannot have its descendant as its parent.")})

        return value

    def is_descendant(self, tag, tag_to_check, visited=None):
        if visited is None:
            visited = set()

        if tag in visited:
            return False

        visited.add(tag)
        for child in tag.children.all():
            if child.public_id.hex == tag_to_check.public_id.hex or \
                    self.is_descendant(child, tag_to_check, visited):
                return True
        return False

    def get_direct_children_count(self, obj):
        return obj.children.count()

    def create(self, validated_data):
        color = validated_data.get('color', None)
        if not color:
            color = self._get_unique_color()
            validated_data['color'] = color

        return super().create(validated_data)

    def update(self, instance, validated_data):
        color = validated_data.get('color', None)
        if not color and not instance.color:
            color = self._get_unique_color()
            validated_data['color'] = color

        return super().update(instance, validated_data)

    def _get_unique_color(self):
        while True:
            color = "%06x" % random.randint(0, 0xFFFFFF)
            try:
                BimaCoreTag.objects.get(color=color)
            except ObjectDoesNotExist:
                return color
