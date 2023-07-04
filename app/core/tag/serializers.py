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
        allow_null=True
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
        fields = ['id', 'name', 'public_id', 'parent', 'parent_public_id', 'color']

    def validate_color(self, value):
        if value and not re.match('^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', value):
            raise serializers.ValidationError(_("This field should be a valid hex color."))
        return value

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

    def to_internal_value(self, data):
        if 'parent_public_id' in data and data['parent_public_id'] == "":
            data['parent_public_id'] = None
        return super().to_internal_value(data)

    def _get_unique_color(self):
        while True:
            color = "%06x" % random.randint(0, 0xFFFFFF)
            try:
                BimaCoreTag.objects.get(color=color)
            except ObjectDoesNotExist:
                return color
