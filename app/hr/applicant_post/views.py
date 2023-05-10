from core.abstract.views import AbstractViewSet

from .serializers import BimaHrApplicantPostSerializer
from .models import BimaHrApplicantPost

class BimaHrApplicantPostViewSet(AbstractViewSet):
    queryset = BimaHrApplicantPost.objects.all()
    serializer_class = BimaHrApplicantPostSerializer
    permission_classes = []
