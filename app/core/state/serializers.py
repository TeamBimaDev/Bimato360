from core.abstract.serializers import AbstractSerializer
from core.state.models import BimaCoreState
from rest_framework import serializers
from core.country.models import BimaCoreCountry
from core.country.serializers import BimaCoreCountrySerializer


class BimaCoreStateSerializer(AbstractSerializer):
    country = BimaCoreCountrySerializer(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=BimaCoreCountry.objects.all(),
        source='country',
        write_only=True
    )
    class Meta:
        model = BimaCoreState
        fields = ['id', 'name', 'code', 'country', 'created', 'updated', 'country_id']

