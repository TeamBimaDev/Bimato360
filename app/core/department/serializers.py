from rest_framework import serializers
from core.abstract.serializers import AbstractSerializer
from .models import BimaCoreDepartment

class BimaCoreDepartmentSerializer(AbstractSerializer):
    parent = serializers.SerializerMethodField()
    parent_id = serializers.SerializerMethodField()



    def get_parent(self, obj):
        if obj.department:
            serializer = self.__class__(obj.department)
            return serializer.data
        return None

    def get_parent_id(self, obj):
        if obj.department:
            return obj.department.public_id
        return None

    def get_children(self, obj):
        serializer = self.__class__(obj.children.all(), many=True)
        return serializer.data

    class Meta:
        model = BimaCoreDepartment
        fields = ('id', 'name', 'description', 'manager', 'parent', 'parent_id')