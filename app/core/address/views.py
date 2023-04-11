from core.abstract.views import AbstractViewSet
from core.address.models import BimaCoreAddress
from core.address.serializers import BimaCoreAddressSerializer


class BimaCoreAddressViewSet(AbstractViewSet):
    queryset = BimaCoreAddress.objects.all()
    serializer_class = BimaCoreAddressSerializer
    permission_classes = []
