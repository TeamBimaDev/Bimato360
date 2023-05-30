from core.abstract.views import AbstractViewSet
from .serializers import  BimaPartnersPaymentSerializer
from .models import BimaPartnersPayment

class BimaPartnersPaymentViewSet(AbstractViewSet):
    queryset = BimaPartnersPayment.objects.all()
    serializer_class = BimaPartnersPaymentSerializer
    permission_classes = []






