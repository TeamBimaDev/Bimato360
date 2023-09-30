from core.abstract.serializers import AbstractSerializer
from hr.employee.models import BimaHrEmployee
from rest_framework import serializers

from .models import BimaHrVacation


class BimaHrVacationSerializer(AbstractSerializer):
    manager = serializers.SerializerMethodField(read_only=True)
    manager_public_id = serializers.SlugRelatedField(
        queryset=BimaHrEmployee.objects.all(),
        slug_field='public_id',
        source='manager',
        write_only=True

    )

    employee = serializers.SerializerMethodField(read_only=True)
    employee_public_id = serializers.SlugRelatedField(
        queryset=BimaHrEmployee.objects.all(),
        slug_field='public_id',
        source='employee',
        write_only=True
    )

    def get_manager(self, obj):
        return {
            'id': obj.manager.public_id.hex,
            'name': obj.manager.full_name,
        }

    def get_employee(self, obj):
        return {
            'id': obj.employee.public_id.hex,
            'name': obj.employee.full_name,
        }

    class Meta:
        model = BimaHrVacation
        fields = [
            'id', 'employee', 'employee_public_id', 'manager', 'manager_public_id', 'date_start', 'date_end',
            'reason', 'vacation_type', 'status', 'reason_refused', 'created', 'updated'
        ]
