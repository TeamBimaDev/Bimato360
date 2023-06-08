from core.abstract.views import AbstractViewSet
from core.contact.models import BimaCoreContact
from core.contact.serializers import BimaCoreContactSerializer


class BimaCoreContactViewSet(AbstractViewSet):
    queryset = BimaCoreContact.objects.all()
    serializer_class = BimaCoreContactSerializer
    permission_classes = []

    def get_object(self):
        obj = BimaCoreContact.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
