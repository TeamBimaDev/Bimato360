from core.abstract.serializers import AbstractSerializer
from core.state.models import BimaCoreState
from rest_framework import serializers
from core.country.models import BimaCoreCountry


class BimaCoreStateSerializer(AbstractSerializer):
    country = serializers.SerializerMethodField(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=BimaCoreCountry.objects.all(),
        source='country',
        write_only=True
    )
    def get_country(self, obj):
        return {
            'id': obj.country.public_id.hex,
            'name': obj.country.name,
            'code': obj.country.code,
        }

    class Meta:
        model = BimaCoreState
        fields = ['id', 'name', 'code', 'country', 'created', 'updated', 'country_id']

