from core.abstract.views import AbstractViewSet
from core.contact.models import BimaCoreContact
from core.permissions import IsAdminOrReadOnly
from core.contact.serializers import BimaCoreContactserializer
from core.pagination import DefaultPagination


class BimaCoreContactViewSet(AbstractViewSet):
    queryset = BimaCoreContact.objects.all()
    serializer_class = BimaCoreContactserializer
    permission_classes = []
    pagination_class = DefaultPagination

    def get_object(self):
        obj = BimaCoreContact.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
