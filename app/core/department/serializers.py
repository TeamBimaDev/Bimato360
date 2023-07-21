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

    def get_direct_children_count(self, obj):
        return obj.children.count()

    def validate_department_public_id(self, value):
        if not value:
            return value

        department_to_edit = self.instance
        try:
            proposed_parent = BimaCoreDepartment.objects.get_object_by_public_id(value)
        except BimaCoreDepartment.DoesNotExist:
            raise serializers.ValidationError("The proposed parent department does not exist.")
     
        if proposed_parent and proposed_parent.department:
            if self.is_descendant(proposed_parent, department_to_edit) or \
               self.is_ancestor(department_to_edit, proposed_parent):
                raise serializers.ValidationError("A department cannot have its descendant as its parent, "
                                                  "or become a parent of its own ancestor.")
        return value

    @staticmethod
    def is_descendant(department, department_to_check):
        for child in department.children.all():
            if child.public_id.hex == department_to_check.public_id.hex or \
               BimaCoreDepartmentSerializer.is_descendant(child, department_to_check):
                return True
        return False

    @staticmethod
    def is_ancestor(department, department_to_check):
        if department.department is None:
            return False
        if department.department.public_id.hex == department_to_check.public_id.hex or \
           BimaCoreDepartmentSerializer.is_ancestor(department.department, department_to_check):
            return True
        return False
