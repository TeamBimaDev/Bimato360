from core.abstract.serializers import AbstractSerializer
from django.contrib.auth.models import Permission
from rest_framework import serializers

from .models import BimaUserRole


class BimaUserRoleSerializer(AbstractSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Permission.objects.all(),
        required=False
    )

    class Meta:
        model = BimaUserRole
        fields = ['id', 'created', 'updated', 'name', 'active', 'note', 'permissions']
