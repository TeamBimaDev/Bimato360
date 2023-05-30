from core.abstract.serializers import AbstractSerializer

from erp.partner.models import BimaErpPartner


class BimaErpPartnerSerializer(AbstractSerializer):
    class Meta:
        model = BimaErpPartner
        fields = '__all__'
