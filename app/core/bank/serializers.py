from core.abstract.serializers import AbstractSerializer
from core.bank.models import BimaCoreBank


class BimaCoreBankSerializer(AbstractSerializer):
    class Meta:
        model = BimaCoreBank
        fields = ['id', 'name', 'street', 'street2', 'zip', 'city', 'state', 'country', 'email', 'active', 'bic', 'created', 'updated']

