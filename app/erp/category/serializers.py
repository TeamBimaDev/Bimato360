from .models import BimaErpCategory
from core.abstract.serializers import AbstractSerializer
from rest_framework import serializers


class BimaErpCategorySerializer(AbstractSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=BimaErpCategory.objects.all(),
        source='category',
        write_only=True,
        required=False
    )

    def get_category(self, obj):
        if obj.category:
            return {
                'id': obj.category.public_id.hex,
                'name': obj.category.name,
            }
        return None

    class Meta:
        model = BimaErpCategory
        fields = ['id', 'name', 'description', 'active', 'public_id', 'category', 'category_id']
