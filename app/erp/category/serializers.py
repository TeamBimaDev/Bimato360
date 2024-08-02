

from .models import BimaErpCategory
from core.abstract.serializers import AbstractSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class BimaErpCategorySerializer(AbstractSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    category_public_id = serializers.SlugRelatedField(
        queryset=BimaErpCategory.objects.all(),
        slug_field='public_id',
        source='category',
        write_only=True,
        required=False,
        allow_empty=True,
        allow_null=True
    )

    direct_children_count = serializers.SerializerMethodField()

    def get_category(self, obj):
        if obj.category:
            return {
                'id': obj.category.public_id.hex,
                'name': obj.category.name,
            }
        return None

    class Meta:
        model = BimaErpCategory
        fields = ['id', 'name', 'description', 'active', 'public_id', 'category', 'category_public_id', \
                  'direct_children_count']

    def to_internal_value(self, data):
        if 'category_public_id' in data and data['category_public_id'] == "":
            data['category_public_id'] = None
        return super().to_internal_value(data)

    def get_direct_children_count(self, obj):
        return obj.children.count()

    def validate_category_public_id(self, value):
        if not value:
            return value

        category_to_edit = self.instance
        proposed_parent = value

        if proposed_parent and self.instance:
            if self.is_descendant(category_to_edit, proposed_parent):
                raise serializers.ValidationError({"Categorie parent":
                                                       _("A Category cannot have its descendant as its parent.")})

        return value

    def is_descendant(self, category, category_to_check, visited=None):

        if visited is None:
            visited = set()

        if category in visited:
            return False

        visited.add(category)
        for child in category.children.all():
            if child.public_id.hex == category_to_check.public_id.hex or \
                    self.is_descendant(child, category_to_check, visited):
                return True
        return False


