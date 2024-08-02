from core.abstract.serializers import AbstractSerializer
from hr.vacancie.models import BimaHrVacancie
from hr.candidat.models import BimaHrCandidat
from .models import BimaHrTechnicalInterview, BimaHrEmployeeinterviewer
from hr.employee.models import BimaHrEmployee
from hr.employee.serializers import BimaHrEmployeeSerializer
from hr.interview_step.models import BimaHrInterviewStep
from rest_framework import serializers
from hr.interview_step.models import BimaHrInterviewStep
from .utils.google_calendar import create_calendar_event, update_calendar_event, delete_calendar_event
from rest_framework.exceptions import ValidationError


class BimaHrTechnicalInterviewSerializer(AbstractSerializer):
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
                'name': obj.candidat.full_name,
                'email':obj.candidat.email
            }
        return None
    
    interviewers = serializers.SlugRelatedField(
        queryset=BimaHrEmployee.objects.all(),
        slug_field='public_id',
        many=True,
        write_only=True
    )
    interviewers_details = serializers.SerializerMethodField(read_only=True)

    def get_interviewers_details(self, obj):
        interviewers = obj.interviewers.all()
        return [{'id': interviewer.public_id.hex, 'first_name': interviewer.first_name, 'last_name': interviewer.last_name, 'email':interviewer.email} for interviewer in interviewers]

    def create(self, validated_data):
        interviewers_data = validated_data.pop('interviewers', [])
        technical_interview = BimaHrTechnicalInterview.objects.create(**validated_data)
        technical_interview.interviewers.set(interviewers_data)
        
        # Create a calendar event
        try:
            event_id, hangout_link = create_calendar_event(technical_interview)
            technical_interview.id_event = event_id
            technical_interview.link_interview = hangout_link
            technical_interview.save()
        except Exception as e:
            raise ValidationError({'calendar': f"Failed to create Google Calendar event: {str(e)}"})
        
        return technical_interview

    def update(self, instance, validated_data):
        interviewers_data = validated_data.pop('interviewers', [])
        instance = super().update(instance, validated_data)
        instance.interviewers.set(interviewers_data)
        # Update calendar event
        try:
            hangout_link = update_calendar_event(instance)
            instance.link_interview = hangout_link
            instance.save()
        except Exception as e:
            raise ValidationError({'calendar': f"Failed to update Google Calendar event: {str(e)}"})

        return instance
    
    class Meta:
        model = BimaHrTechnicalInterview
        fields = [
            'id', 'title', 'description', 'start_datetime', 'end_datetime',
            'candidat', 'status', 'vacancie', 'location', 'interview_mode',
            'candidat_public_id', 'link_interview', 'interview_step',
            'vacancie_public_id', 'interview_step_public_id', 'record_path',
            'created', 'updated', 'interviewers', 'interviewers_details'
        ]
        extra_kwargs = {
            'interviewers': {'write_only': True},
            'interviewers_details': {'read_only': True},
        }

