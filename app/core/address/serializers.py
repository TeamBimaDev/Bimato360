from core.address.models import BimaCoreAddress
from core.abstract.serializers import AbstractSerializer
from core.country.models import BimaCoreCountry
from rest_framework import serializers
from core.state.models import BimaCoreState


class BimaCoreAddressSerializer(AbstractSerializer):
    country = serializers.SerializerMethodField(read_only=True)
    country_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreCountry.objects.all(),
        slug_field='public_id',
        source='country',
        write_only=True
    )

    def get_country(self, obj):
        return {
            'id': obj.country.public_id.hex,
            'name': obj.country.name,
        }

    state = serializers.SerializerMethodField(read_only=True)
    state_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreState.objects.all(),
        slug_field='public_id',
        source='state',
        write_only=True
    )

    def get_state(self, obj):
        return {
            'id': obj.state.public_id.hex,
            'name': obj.state.name,
        }

    class Meta:
        model = BimaCoreAddress
        fields = [
            'id', 'number', 'street', 'street2', 'zip', 'city', 'state',
            'contact_name', 'contact_phone', 'contact_email', 'can_send_bill',
            'can_deliver', 'latitude', 'longitude', 'note',
            'country', 'country_public_id', 'state_public_id', 'created', 'updated'
        ]
