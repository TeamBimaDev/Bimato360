from rest_framework import serializers
from core.abstract.serializers import AbstractSerializer
from .models import BimaCoreDepartment
from django.utils.translation import gettext_lazy as _


class BimaCoreDepartmentSerializer(AbstractSerializer):
    department = serializers.SerializerMethodField(read_only=True)
    department_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreDepartment.objects.all(),
        slug_field='public_id',
        source='department',
        write_only=True,
        required=False
    )
    direct_children_count = serializers.SerializerMethodField()

    class Meta:
        model = BimaCoreDepartment
        fields = ['id', 'name', 'description', 'public_id', 'department',
                  'department_public_id', 'manager', 'direct_children_count']

    def get_department(self, obj):
        if obj.department:
            return {
                'id': obj.department.public_id.hex,
                'name': obj.department.name,
            }
        return None

    def to_internal_value(self, data):
        if 'department_public_id' in data and data['department_public_id'] == "":
            data['department_public_id'] = None
        return super().to_internal_value(data)

    def get_direct_children_count(self, obj):
        return obj.children.count()

    def validate_department_public_id(self, value):
        if not value:
            return value

        department_to_edit = self.instance
        proposed_parent = value

        if proposed_parent:
            if self.is_descendant(department_to_edit, proposed_parent):
                raise serializers.ValidationError({"Departement parent":
                                                       _("A department cannot have its descendant as its parent.")})

        return value

    def is_descendant(self, department, department_to_check, visited=None):

        if visited is None:
            visited = set()

        if department in visited:
            return False

        visited.add(department)
        for child in department.children.all():
            if child.public_id.hex == department_to_check.public_id.hex or \
                    self.is_descendant(child, department_to_check, visited):
                return True
        return False
