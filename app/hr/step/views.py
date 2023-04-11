from core.abstract.views import AbstractViewSet
from .models import BimaHrInterviewStep
from .serializers import BimaHrInterviewStepSerializer


class BimaHrInterviewViewStepSet(AbstractViewSet):
    queryset = BimaHrInterviewStep.objects.all()
    serializer_class = BimaHrInterviewStepSerializer
    permission_classes = []

