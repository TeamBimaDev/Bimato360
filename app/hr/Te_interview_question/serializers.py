from core.abstract.serializers import AbstractSerializer
from hr.technical_interview.models import BimaHrTechnicalInterview
from rest_framework import serializers

from .models import BimaHrTechnicalInterviewQuestion


class BimaHrTechnicalInterviewQuestionSerializer(AbstractSerializer):
    interview_te = serializers.SerializerMethodField(read_only=True)
    interview_public_id_te = serializers.SlugRelatedField(
        queryset=BimaHrTechnicalInterview.objects.all(),
        slug_field='public_id',
        source='technical_interview',
        write_only=True
    )

    def get_tech_interview(self, obj):
        return {
            'id': obj.tech_interview.public_id.hex,
            'name': obj.tech_interview.name,
        }

    class Meta:
        model = BimaHrTechnicalInterviewQuestion
        fields = [
            'id', 'question_te','response_te', 'interview_te', 'interview_public_id_te', 'created', 'updated'
        ]
