from common.converters.default_converters import str_to_bool
from core.abstract.serializers import AbstractSerializer
from hr.skill.models import BimaHrSkill
from rest_framework import serializers

from .models import BimaHrPerson, BimaHrPersonExperience


class BimaHrSerializer(AbstractSerializer):
    class Meta:
        model = BimaHrPerson
        fields = [
            'id', 'unique_id', 'gender', 'first_name', 'last_name',
            'date_of_birth', 'place_of_birth', 'created', 'updated'
        ]


class BimaHrPersonExperienceSerializer(AbstractSerializer):
    experience_duration = serializers.ReadOnlyField()
    person = serializers.SerializerMethodField(read_only=True)
    person_public_id = serializers.SlugRelatedField(
        queryset=BimaHrPerson.objects.all(),
        slug_field='public_id',
        source='person',
        write_only=True
    )

    def get_person(self, obj):
        if obj.person:
            return {
                'id': obj.person.public_id.hex,
                'name': obj.person.full_name,
            }
        return None

    def save(self, **kwargs):
        is_current_position = str_to_bool(self.validated_data.get('is_current_position', False))
        if is_current_position:
            self.validated_data['date_end'] = None

        return super().save(**kwargs)

    class Meta:
        model = BimaHrPersonExperience
        fields = [
            'id', 'person', 'person_public_id', 'company_name', 'position', 'description',
            'date_begin', 'date_end', 'is_current_position', 'experience_duration', 'created', 'updated'
        ]


class BimaHrPersonSkillSerializer(AbstractSerializer):
    person = serializers.SerializerMethodField(read_only=True)
    person_public_id = serializers.SlugRelatedField(
        queryset=BimaHrPerson.objects.all(),
        slug_field='public_id',
        source='person',
        write_only=True
    )
    skill = serializers.SerializerMethodField(read_only=True)
    skill_public_id = serializers.SlugRelatedField(
        queryset=BimaHrSkill.objects.all(),
        slug_field='public_id',
        source='skill',
        write_only=True
    )

    def get_person(self, obj):
        if obj.person:
            return {
                'id': obj.person.public_id.hex,
                'name': obj.person.full_name,
            }
        return None

    def get_skill(self, obj):
        if obj.skill:
            return {
                'id': obj.skill.public_id.hex,
                'name': obj.skill.name,
            }
        return None

    class Meta:
        model = BimaHrPersonExperience
        fields = [
            'id', 'person', 'person_public_id', 'company_name', 'skill', 'skill_public_id', 'description', 'date_begin',
            'date_end', 'is_current_position', 'created', 'updated'
        ]
