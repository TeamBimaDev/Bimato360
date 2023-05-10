from core.abstract.serializers import AbstractSerializer
from partners.partners.models import BimaPartners


class BimaPartnersSerializer(AbstractSerializer):
    class Meta:
        model = BimaPartners
        fields = '__all__'