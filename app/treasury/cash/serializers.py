from company.models import BimaCompany
from core.abstract.serializers import AbstractSerializer
from rest_framework import serializers

from .models import BimaTreasuryCash


class BimaTreasuryCashSerializer(AbstractSerializer):
    company = serializers.SerializerMethodField(read_only=True)
    company_public_id = serializers.SlugRelatedField(
        queryset=BimaCompany.objects.all(),
        slug_field='public_id',
        source='company',
        write_only=True
    )

    def get_company(self, obj):
        return {
            'id': obj.company.public_id.hex,
            'name': obj.company.name,
        }

    class Meta:
        model = BimaTreasuryCash
        fields = [
            'id', 'name', 'active', 'note', 'company', 'company_public_id', 'created', 'updated', 'balance'
        ]
        read_only_fields = ('balance',)
