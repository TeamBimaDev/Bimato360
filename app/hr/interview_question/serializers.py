from core.abstract.serializers import AbstractSerializer
from hr.interview.models import BimaHrInterview
from rest_framework import serializers

from .models import BimaHrInterviewQuestion


class BimaHrInterviewQuestionSerializer(AbstractSerializer):
    interview = serializers.SerializerMethodField(read_only=True)
    interview_public_id = serializers.SlugRelatedField(
        queryset=BimaHrInterview.objects.all(),
        slug_field='public_id',
        source='interview',
        write_only=True
    )

    def get_interview(self, obj):
        return {
            'id': obj.interview.public_id.hex,
            'name': obj.interview.name,
        }

    class Meta:
        model = BimaHrInterviewQuestion
        fields = [
            'id', 'question','response', 'interview', 'interview_public_id', 'created', 'updated'
        ]
