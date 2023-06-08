from core.abstract.views import AbstractViewSet
from core.address.models import BimaCoreAddress
from core.address.serializers import BimaCoreAddressSerializer


class BimaCoreAddressViewSet(AbstractViewSet):
    queryset = BimaCoreAddress.objects.select_related('state', 'country').all()
    serializer_class = BimaCoreAddressSerializer
    permission_classes = []

    def get_object(self):
        obj = BimaCoreAddress.objects. \
            get_object_by_public_id(self.kwargs['pk'])
        return obj
