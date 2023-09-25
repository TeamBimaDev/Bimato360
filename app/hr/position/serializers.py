from core.abstract.serializers import AbstractSerializer
from core.department.models import BimaCoreDepartment
from hr.employee.models import BimaHrEmployee
from hr.job_category.models import BimaHrJobCategory
from rest_framework import serializers

from .models import BimaHrPosition


class BimaHrPositionSerializer(AbstractSerializer):
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
        write_only=True
    )

    def get_department(self, obj):
        return {
            'id': obj.department.public_id.hex,
            'name': obj.department.name,
        }

    def get_department(self, obj):
        if self.job_category:
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
        model = BimaHrPosition
        fields = [
            'id', 'title', 'description', 'requirements', 'responsibilities',
            'department', 'department_public_id', 'job_category', 'job_category_public_id',
            'manager', 'manager_public_id', 'created', 'updated'
        ]
