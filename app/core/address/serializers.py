from core.address.models import BimaCoreAddress
from core.abstract.serializers import AbstractSerializer
from core.country.serializers import BimaCoreCountrySerializer
from core.country.models import BimaCoreCountry
from rest_framework import serializers
from core.state.models import BimaCoreState
from core.state.serializers import BimaCoreStateSerializer


class BimaCoreAddressSerializer(AbstractSerializer):
    country = serializers.SerializerMethodField(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=BimaCoreCountry.objects.all(),
        source='country',
        write_only=True
    )
    state =serializers.SerializerMethodField(read_only=True)
    state_id = serializers.PrimaryKeyRelatedField(
        queryset=BimaCoreState.objects.all(),
        source='state',
        write_only=True
    )

    def get_country(self, obj):
        return {
            'id': obj.country.public_id.hex,
            'name': obj.country.name,
            'code': obj.country.code,
        }

    def get_state(self, obj):
        return {
            'id': obj.state.public_id.hex,
            'name': obj.state.name,
            'code': obj.state.code,
        }

    class Meta:
        model = BimaCoreAddress
        fields = [
            'id', 'number', 'street', 'street2', 'zip', 'city', 'state',
            'country', 'country_id', 'state_id', 'created', 'updated'
        ]
