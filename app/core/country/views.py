from core.abstract.views import AbstractViewSet
from core.country.models import BimaCoreCountry
from core.permissions import IsAdminOrReadOnly
from core.country.serializers import BimaCoreCountrySerializer


class BimaCoreCountryViewSet(AbstractViewSet):
    queryset = BimaCoreCountry.objects.all()
    serializer_class = BimaCoreCountrySerializer
    permission_classes = []
