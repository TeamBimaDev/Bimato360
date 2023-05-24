from core.abstract.serializers import AbstractSerializer
from .models import BimaCorePost
from core.department.serializers import BimaCoreDepartmentSerializer
from rest_framework import serializers
from core.department.models import BimaCoreDepartment


class BimaCorePostSerializer(AbstractSerializer):
    department = BimaCoreDepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=BimaCoreDepartment.objects.all(),
        source='department',
        write_only=True
    )
    class Meta:
        model = BimaCorePost
        fields = [
            'id', 'name', 'description', 'requirements', 'responsibilities', 'department', 'department_id', 'created', 'updated'
        ]