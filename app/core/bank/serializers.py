from core.abstract.serializers import AbstractSerializer
from core.bank.models import BimaCoreBank


class BimaCoreBankSerializer(AbstractSerializer):
    class Meta:
        model = BimaCoreBank
        fields = '__all__'
