from core.abstract.views import AbstractViewSet
from company.models import BimaCompany
from company.serializers import BimaCompanySerializer


class BimaCompanyViewSet(AbstractViewSet):
    queryset = BimaCompany.objects.all()
    serializer_class = BimaCompanySerializer
    permission_classes = []
