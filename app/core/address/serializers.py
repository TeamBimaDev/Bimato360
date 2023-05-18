from core.address.models import BimaCoreAddress
from core.abstract.serializers import AbstractSerializer
from core.country.serializers import BimaCoreCountrySerializer
from core.country.models import BimaCoreCountry
from rest_framework import serializers
from core.state.models import BimaCoreState
from core.state.serializers import BimaCoreStateSerializer


class BimaCoreAddressSerializer(AbstractSerializer):
    country = BimaCoreCountrySerializer(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=BimaCoreCountry.objects.all(),
        source='country',
        write_only=True
    )
    state = BimaCoreStateSerializer(read_only=True)
    state_id = serializers.PrimaryKeyRelatedField(
        queryset=BimaCoreState.objects.all(),
        source='state',
        write_only=True
    )
    class Meta:
        model = BimaCoreAddress
        fields = [
            'number', 'street', 'street2', 'zip', 'city', 'state',
            'country', 'country_id', 'state_id', 'created', 'updated'
        ]
