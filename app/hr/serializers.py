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
        if self.person:
            return {
                'id': obj.person.public_id.hex,
                'name': obj.person.get_full_name,
            }
        return None

    def get_skill(self, obj):
        if self.skill:
            return {
                'id': obj.skill.public_id.hex,
                'name': obj.skill.name,
            }
        return None

    class Meta:
        model = BimaHrPersonExperience
        fields = [
            'id', 'person', 'person_public_id', 'skill', 'skill_public_id', 'company_name', 'description', 'date_begin',
            'date_end', 'is_current_position', 'created', 'updated'
        ]


class BimaHrPersonSkillSerializer(AbstractSerializer):
    person = serializers.SerializerMethodField(read_only=True)
    person_public_id = serializers.SlugRelatedField(
        queryset=BimaHrPerson.objects.all(),
        slug_field='public_id',
        source='person',
        write_only=True
    )

    def get_person(self, obj):
        if self.person:
            return {
                'id': obj.person.public_id.hex,
                'name': obj.person.get_full_name,
            }
        return None

    class Meta:
        model = BimaHrPersonExperience
        fields = [
            'id', 'person', 'person_public_id', 'company_name', 'description', 'date_begin',
            'date_end', 'is_current_position', 'created', 'updated'
        ]
