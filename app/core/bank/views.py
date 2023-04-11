from core.abstract.views import AbstractViewSet
from core.bank.models import BimaCoreBank
from core.permissions import IsAdminOrReadOnly
from core.bank.serializers import BimaCoreBankSerializer


class BimaCoreBankViewSet(AbstractViewSet):
    queryset = BimaCoreBank.objects.all()
    serializer_class = BimaCoreBankSerializer
    permission_classes = [IsAdminOrReadOnly]
