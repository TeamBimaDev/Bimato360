from datetime import datetime
from core.country.models import BimaCoreCountry
from core.abstract.serializers import AbstractSerializer
from rest_framework import serializers

from .models import BimaHrCandidat


class BimaHrCandidatSerializer(AbstractSerializer):
    full_name = serializers.ReadOnlyField()
    country = serializers.SerializerMethodField(read_only=True)
    country_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreCountry.objects.all(),
        slug_field='public_id',
        source='country',
        write_only=True
    )

    def get_country(self, obj):
        if obj.country:
            return {
                'id': obj.country.public_id.hex,
                'name': obj.country.name,
            }
        return None

    class Meta:
        model = BimaHrCandidat
        fields = [
            'id', 'unique_id', 'gender', 'marital_status', 'first_name', 'last_name', 'date_of_birth',
            'place_of_birth', 'country', 'full_name', 'country_public_id','nationality', 'identity_card_number', 'phone_number', 
            'second_phone_number', 'email', 'education_level', 'latest_degree', 'latest_degree_date', 'institute',  'availability_days', 
            'message', 'created', 'updated'
        ]

      
        
        
   