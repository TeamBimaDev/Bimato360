from rest_framework import serializers
from core.abstract.serializers import AbstractSerializer
from .models import BimaCoreDepartment


class BimaCoreDepartmentSerializer(AbstractSerializer):
    department = serializers.SerializerMethodField(read_only=True)
    department_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreDepartment.objects.all(),
        slug_field='public_id',
        source='department',
        write_only=True,
        required=False
    )
    all_parents = serializers.SerializerMethodField(read_only=True)
    all_children = serializers.SerializerMethodField(read_only=True)

    def get_department(self, obj):
        if obj.department:
            return {
                'id': obj.department.public_id.hex,
                'name': obj.department.name,
            }
        return None

    def get_all_parents(self, obj):
        parents = []
        current = obj.department
        visited = set()
        while current and current.public_id not in visited:
            visited.add(current.public_id)
            parents.append({
                'id': current.public_id.hex,
                'name': current.name,
            })
            current = current.department if hasattr(current, 'department') else None
        return parents

    def get_all_children(self, obj):
        def get_descendants(department, visited):
            children = []
            for child in department.children.all():
                if child.public_id not in visited:
                    visited.add(child.public_id)
                    children.append({
                        'id': child.public_id.hex,
                        'name': child.name,
                    })
                    children.extend(get_descendants(child, visited))
            return children

        return get_descendants(obj, set())

    class Meta:
        model = BimaCoreDepartment
        fields = ['id', 'name', 'description', 'public_id', 'department',
                  'department_public_id', 'manager', 'all_parents', 'all_children']
