from core.abstract.views import AbstractViewSet
from core.contact.models import BimaCoreContact
from core.permissions import IsAdminOrReadOnly
from core.contact.serializers import BimaCoreContactserializer


class BimaCoreContactViewSet(AbstractViewSet):
    queryset = BimaCoreContact.objects.all()
    serializer_class = BimaCoreContactserializer
    permission_classes = []
