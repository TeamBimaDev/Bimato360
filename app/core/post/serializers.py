from core.abstract.serializers import AbstractSerializer
from .models import BimaCorePost
from rest_framework import serializers
from core.department.models import BimaCoreDepartment


class BimaCorePostSerializer(AbstractSerializer):
    department = serializers.SerializerMethodField(read_only=True)
    department_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreDepartment.objects.all(),
        slug_field='public_id',
        source='department',
        write_only=True
    )

    def get_department(self, obj):
        return {
            'id': obj.department.public_id.hex,
            'name': obj.department.name,
        }

    class Meta:
        model = BimaCorePost
        fields = [
            'id', 'name', 'description', 'requirements', 'responsibilities',
            'department', 'department_public_id', 'created', 'updated'
        ]
