from core.abstract.serializers import AbstractSerializer
from core.department.models import BimaCoreDepartment
from hr.employee.models import BimaHrEmployee
from hr.job_category.models import BimaHrJobCategory
from rest_framework import serializers

from .models import BimaHrVacancie, BimaHrCandidatVacancie
from hr.candidat.models import BimaHrCandidat


class BimaHrVacancieSerializer(AbstractSerializer):
    department = serializers.SerializerMethodField(read_only=True)
    department_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreDepartment.objects.all(),
        slug_field='public_id',
        source='department',
        write_only=True
    )

    job_category = serializers.SerializerMethodField(read_only=True)
    job_category_public_id = serializers.SlugRelatedField(
        queryset=BimaHrJobCategory.objects.all(),
        slug_field='public_id',
        source='job_category',
        write_only=True
    )

    manager = serializers.SerializerMethodField(read_only=True)
    manager_public_id = serializers.SlugRelatedField(
        queryset=BimaHrEmployee.objects.all(),
        slug_field='public_id',
        source='manager',
        write_only=True,
        required=False,
        allow_empty=True,
        allow_null=True
    )

    def get_department(self, obj):
        return {
            'id': obj.department.public_id.hex,
            'name': obj.department.name,
        }

    def get_job_category(self, obj):
        if obj.job_category:
            return {
                'id': obj.job_category.public_id.hex,
                'name': obj.job_category.name,
            }
        return None

    def get_manager(self, obj):
        if obj.manager:
            return {
                'id': obj.manager.public_id.hex,
                'name': obj.manager.full_name
            }
        return None

   
    class Meta:
        model = BimaHrVacancie
        fields = [
            'id', 'title', 'description', 'seniority', 'work_mode', 'job_type', 'date_expiration', 'date_start_vacancie', 
            'department', 'number_of_positions', 'published_date', 'department_public_id', 'job_category', 'job_category_public_id', 
            'work_location', 'manager', 'manager_public_id', 'position_status', 'created', 'updated', 'number_of_candidates'
        ]

    def validate(self, data):
                self.validate_date_range(data)
                return data

    def validate_date_range(self, data):
                published_date = data.get('published_date')
                date_expiration = data.get('date_expiration')
                date_start_vacancie = data.get('date_start_vacancie')

                if published_date and date_expiration:
                    if published_date >= date_expiration:
                        raise serializers.ValidationError({
                            "published_date": "Published date must be before the expiration date."
                        })

                if date_expiration and date_start_vacancie:
                    if date_expiration <= date_start_vacancie:
                        raise serializers.ValidationError({
                            "date_expiration": "Expiration date must be after the start date."
                        })    
    

class BimaHrCandidatVacancieSerializer(AbstractSerializer):
    vacancie = BimaHrVacancieSerializer(read_only=True)
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
        write_only=True,
        required=False  # Marquer comme non requis
    )

    def get_candidat(self, obj):
        from hr.candidat.serializers import BimaHrCandidatSerializer  # Importation tardive
        serializer = BimaHrCandidatSerializer(obj.candidat)
        return serializer.data

    class Meta:
        model = BimaHrCandidatVacancie
        fields = [
            'id', 'vacancie', 'vacancie_public_id', 'candidat', 'candidat_public_id', 'expected_salary',
            'proposed_salary', 'accepted_salary', 'date', 'comments', 'score', 'created', 'updated'
        ]

    def create(self, validated_data):
        vacancie = validated_data.pop('vacancie', None)
        if not vacancie:
            vacancie = self.context.get('vacancie')
        validated_data['vacancie'] = vacancie
        return super().create(validated_data)
 
   
