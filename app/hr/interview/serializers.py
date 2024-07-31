<<<<<<< HEAD
from core.abstract.serializers import AbstractSerializer
from hr.vacancie.models import BimaHrVacancie
from hr.candidat.models import BimaHrCandidat
from hr.interview.models import BimaHrInterview
from hr.interview_step.models import BimaHrInterviewStep
from rest_framework import serializers
from hr.interview_step.models import BimaHrInterviewStep


class BimaHrInterviewSerializer(AbstractSerializer):
    vacancie = serializers.SerializerMethodField(read_only=True)
    vacancie_public_id = serializers.SlugRelatedField(
        queryset=BimaHrVacancie.objects.all(),
        slug_field='public_id',
        source='vacancie',
        write_only=True
    )

    candidat = serializers.SerializerMethodField(read_only=True)
    candidat_public_id = serializers.SlugRelatedField(
        queryset=BimaHrCandidat.objects.all(),
        slug_field='public_id',
        source='candidat',
        write_only=True
    )
    
    interview_step = serializers.SerializerMethodField(read_only=True)
    interview_step_public_id = serializers.SlugRelatedField(
        queryset=BimaHrInterviewStep.objects.all(),
        slug_field='public_id',
        source='interview_step',
        write_only=True
    )

    def get_interview_step(self, obj):
        if obj.interview_step:
            return {
                'id': obj.interview_step.public_id.hex,
                'name': obj.interview_step.name
            }
        return None


    def get_vacancie(self, obj):
        if obj.vacancie:
            return {
                'id': obj.vacancie.public_id.hex,
                'name': obj.vacancie.title
            }
        return None

    def get_candidat(self, obj):
        if obj.candidat:
            return {
                'id': obj.candidat.public_id.hex,
                'name': obj.candidat.full_name
            }
        return None

    

    class Meta:
        model = BimaHrInterview
        fields = [
            'id', 'name','due_date', 'scheduled_date' ,  'score', 'candidat', 'status', 'vacancie', 'vacancie_public_id',
            'candidat_public_id', 'link_interview','estimated_time' ,'interview_step', 'interview_step_public_id','created','updated'
        ]
=======
from core.abstract.serializers import AbstractSerializer
from hr.vacancie.models import BimaHrVacancie
from hr.candidat.models import BimaHrCandidat
from hr.interview.models import BimaHrInterview
from hr.interview_step.models import BimaHrInterviewStep
from rest_framework import serializers
from hr.interview_step.models import BimaHrInterviewStep


class BimaHrInterviewSerializer(AbstractSerializer):
    vacancie = serializers.SerializerMethodField(read_only=True)
    vacancie_public_id = serializers.SlugRelatedField(
        queryset=BimaHrVacancie.objects.all(),
        slug_field='public_id',
        source='vacancie',
        write_only=True
    )

    candidat = serializers.SerializerMethodField(read_only=True)
    candidat_public_id = serializers.SlugRelatedField(
        queryset=BimaHrCandidat.objects.all(),
        slug_field='public_id',
        source='candidat',
        write_only=True
    )
    
    interview_step = serializers.SerializerMethodField(read_only=True)
    interview_step_public_id = serializers.SlugRelatedField(
        queryset=BimaHrInterviewStep.objects.all(),
        slug_field='public_id',
        source='interview_step',
        write_only=True
    )

    def get_interview_step(self, obj):
        if obj.interview_step:
            return {
                'id': obj.interview_step.public_id.hex,
                'name': obj.interview_step.name
            }
        return None


    def get_vacancie(self, obj):
        if obj.vacancie:
            return {
                'id': obj.vacancie.public_id.hex,
                'name': obj.vacancie.title
            }
        return None

    def get_candidat(self, obj):
        if obj.candidat:
            return {
                'id': obj.candidat.public_id.hex,
                'name': obj.candidat.full_name
            }
        return None

    

    class Meta:
        model = BimaHrInterview
        fields = [
            'id', 'name','due_date', 'scheduled_date' ,  'score', 'candidat', 'status', 'vacancie', 'vacancie_public_id',
            'candidat_public_id', 'link_interview','estimated_time' ,'interview_step', 'interview_step_public_id','created','updated'
        ]
>>>>>>> origin/ma-branch
