from core.abstract.serializers import AbstractSerializer
from core.country.models import BimaCoreCountry
from rest_framework import serializers

from .models import BimaHrEmployee


class BimaHrEmployeeSerializer(AbstractSerializer):
    country = serializers.SerializerMethodField(read_only=True)
    country_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreCountry.objects.all(),
        slug_field='public_id',
        source='country',
        write_only=True
    )

    def get_country(self, obj):
        if self.country:
            return {
                'id': obj.country.public_id.hex,
                'name': obj.country.name,
            }
        return None

    class Meta:
        model = BimaHrEmployee
        fields = [
            'id', 'unique_id', 'gender', 'first_name', 'last_name', 'date_of_birth', 'place_of_birth', 'country',
            'country_public_id', 'nationality', 'identity_card_number', 'phone_number', 'second_phone_number', 'email',
            'education_level', 'latest_degree', 'latest_degree_date', 'institute', 'created', 'updated'
        ]
