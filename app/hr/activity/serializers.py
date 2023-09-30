from core.abstract.serializers import AbstractSerializer
from .models import BimaHrActivity
from hr.employee.models import BimaHrEmployee
from rest_framework import serializers
from hr.activity_type.models import BimaHrActivityType


class BimaHrActivitySerializer(AbstractSerializer):
    employee = serializers.SerializerMethodField(read_only=True)
    employee_public_id = serializers.SlugRelatedField(
        queryset=BimaHrEmployee.objects.all(),
        slug_field='public_id',
        source='employee',
        write_only=True
    )
    def get_employee(self, obj):
        return {
            'id': obj.employee.public_id.hex,
            'name': obj.employee.name,
        }
    activity_type = serializers.SerializerMethodField(read_only=True)
    activity_type_public_id = serializers.SlugRelatedField(
        queryset=BimaHrActivityType.objects.all(),
        slug_field='public_id',
        source='activity_type',
        write_only=True
    )
    def get_activity_type(self, obj):
        return {
            'id': obj.activity_type.public_id.hex,
            'name': obj.activity_type.name,
        }
    class Meta:
        model = BimaHrActivity
        fields = [
            'id', 'name', 'description', 'activity_status', 'start_date', 'end_date', 'id_manager', 'activity_type',
            'activity_type_public_id', 'employee', 'employee_public_id', 'position_public_id', 'created', 'updated'
        ]
