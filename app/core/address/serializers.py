from core.address.models import BimaCoreAddress
from core.abstract.serializers import AbstractSerializer
class BimaCoreAddressSerializer(AbstractSerializer):
    class Meta:
        model = BimaCoreAddress
        fields = '__all__'
