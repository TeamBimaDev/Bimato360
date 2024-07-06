from core.abstract.serializers import AbstractSerializer
from core.country.models import BimaCoreCountry
from core.source.models import BimaCoreSource
from core.source.serializers import BimaCoreSourceSerializer
from hr.interview_step.models import BimaHrInterviewStep
from hr.position.models import BimaHrPosition
from hr.position.serializers import BimaHrPositionSerializer
from rest_framework import serializers

from .models import BimaHrApplicant


class BimaHrApplicantSerializer(AbstractSerializer):
    full_name = serializers.ReadOnlyField()
    country = serializers.SerializerMethodField(read_only=True)
    country_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreCountry.objects.all(),
        slug_field='public_id',
        source='country',
        write_only=True
    )

    def get_country(self, obj):
        if obj.country:
            return {
                'id': obj.country.public_id.hex,
                'name': obj.country.name,
            }
        return None

    class Meta:
        model = BimaHrApplicant
        fields = [
            'id', 'unique_id', 'gender', 'marital_status', 'num_children', 'first_name', 'last_name', 'date_of_birth',
            'place_of_birth', 'country', 'full_name', 'country_public_id', 'nationality', 'identity_card_number',
            'phone_number', 'second_phone_number', 'email', 'education_level', 'latest_degree', 'latest_degree_date',
            'institute', 'priority', 'availability_days', 'description', 'comments', 'created', 'updated'
        ]


class BimaHrApplicantPostSerializer(AbstractSerializer):
    position = BimaHrPositionSerializer(read_only=True)
    position_public_id = serializers.SlugRelatedField(
        queryset=BimaHrPosition.objects.all(),
        slug_field='public_id',
        source='position',
        write_only=True
    )

    applicant = BimaHrApplicantSerializer(read_only=True)
    applicant_public_id = serializers.SlugRelatedField(
        queryset=BimaHrApplicant.objects.all(),
        slug_field='public_id',
        source='applicant',
        write_only=True
    )

    source_type = BimaCoreSourceSerializer(read_only=True)
    source_type_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreSource.objects.all(),
        slug_field='public_id',
        source='source_type',
        write_only=True
    )

    interview_step = serializers.SerializerMethodField(read_only=True)
    interview_step_public_id = serializers.SlugRelatedField(
        queryset=BimaHrInterviewStep.objects.all(),
        slug_field='public_id',
        source='interview_step',
        write_only=True
    )

    def get_country(self, obj):
        if self.interview_step:
            return {
                'id': obj.interview_step.public_id.hex,
                'name': obj.interview_step.name,
            }
        return None

    class Meta:
        model = BimaHrApplicant
        fields = [
            'id', 'position', 'position_public_id', 'applicant', 'applicant_public_id', 'expected_salary',
            'proposed_salary', 'accepted_salary', 'date', 'comments', 'source_type', 'source_type_public_id',
            'source_name', 'score', 'interview_step', 'interview_step_public_id', 'created', 'updated'
        ]
