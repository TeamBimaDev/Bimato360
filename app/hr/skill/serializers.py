from core.abstract.serializers import AbstractSerializer
from hr.skill_category.models import BimaHrSkillCategory
from rest_framework import serializers

from .models import BimaHrSkill


class BimaHrSkillSerializer(AbstractSerializer):
    skill_category = serializers.SerializerMethodField(read_only=True)
    skill_category_public_id = serializers.SlugRelatedField(
        queryset=BimaHrSkillCategory.objects.all(),
        slug_field='public_id',
        source='skill_category',
        write_only=True
    )

    def get_skill_category(self, obj):
        return {
            'id': obj.skill_category.public_id.hex,
            'name': obj.skill_category.name,
        }

    class Meta:
        model = BimaHrSkill
        fields = [
            'id', 'name', 'skill_category', 'skill_category_public_id', 'created', 'updated'
        ]
