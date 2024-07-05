from core.abstract.serializers import AbstractSerializer
from hr.question_category.models import BimaHrQuestionCategory
from rest_framework import serializers

from .models import BimaHrQuestion


class BimaHrQuestionSerializer(AbstractSerializer):
    question_category = serializers.SerializerMethodField(read_only=True)
    question_category_public_id = serializers.SlugRelatedField(
        queryset=BimaHrQuestionCategory.objects.all(),
        slug_field='public_id',
        source='question_category',
        write_only=True
    )

    def get_question_category(self, obj):
        return {
            'id': obj.question_category.public_id.hex,
            'name': obj.question_category.name,
        }

    class Meta:
        model = BimaHrQuestion
        fields = [
            'id', 'name', 'question_category', 'question_category_public_id', 'created', 'updated'
        ]
