from core.abstract.serializers import AbstractSerializer
from hr.employee.models import BimaHrEmployee
from hr.interview.models import BimaHrInterview
from hr.interview_step.models import BimaHrInterviewStep
from rest_framework import serializers


class BimaHrInterviewSerializer(AbstractSerializer):
    interviewer = serializers.SerializerMethodField(read_only=True)
    interviewer_public_id = serializers.SlugRelatedField(
        queryset=BimaHrEmployee.objects.all(),
        slug_field='public_id',
        source='interviewer',
        write_only=True
    )

    interview_step = serializers.SerializerMethodField(read_only=True)
    interview_step_public_id = serializers.SlugRelatedField(
        queryset=BimaHrInterviewStep.objects.all(),
        slug_field='public_id',
        source='interview_step',
        write_only=True
    )

    refused_by = serializers.SerializerMethodField(read_only=True)
    refused_by_public_id = serializers.SlugRelatedField(
        queryset=BimaHrEmployee.objects.all(),
        slug_field='public_id',
        source='refused_by',
        write_only=True
    )

    def get_interviewer(self, obj):
        if obj.interviewer:
            return {
                'id': obj.interviewer.public_id.hex,
                'name': obj.interviewer.full_name
            }
        return None

    def get_interview_step(self, obj):
        if obj.interview_step:
            return {
                'id': obj.interview_step.public_id.hex,
                'name': obj.interview_step.name
            }
        return None

    def get_refused_by(self, obj):
        if obj.refused_by:
            return {
                'id': obj.refused_by.public_id.hex,
                'name': obj.refused_by.full_name
            }
        return None

    class Meta:
        model = BimaHrInterview
        fields = [
            'id', 'date', 'interviewer', 'interviewer_public_id', 'note', 'score', 'comments', 'status',
            'interview_step', 'interview_step_public_id', 'applicant_post', 'applicant_post_public_id', 'created',
            'updated'
        ]
