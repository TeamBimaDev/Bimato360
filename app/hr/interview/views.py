from core.abstract.views import AbstractViewSet
from hr.interview.models import BimaHrInterview
from hr.interview.serializers import BimaHrInterviewSerializer


class BimaHrInterviewViewSet(AbstractViewSet):
    queryset = BimaHrInterview.objects.all()
    serializer_class = BimaHrInterviewSerializer
    permission_classes = []
