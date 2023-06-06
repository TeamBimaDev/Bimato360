from rest_framework import serializers
from core.abstract.serializers import AbstractSerializer
from .models import BimaCoreDepartment


class BimaCoreDepartmentSerializer(AbstractSerializer):
    department = serializers.SerializerMethodField(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=BimaCoreDepartment.objects.all(),
        source='department',
        write_only=True,
        required=False
    )

    def get_department(self, obj):
        if obj.department:
            return {
                'id': obj.department.public_id.hex,
                'name': obj.department.name,
            }
        return None

    class Meta:
        model = BimaCoreDepartment
        fields = ['id', 'name', 'description', 'public_id', 'department', 'department_id', 'manager']
