from core.abstract.views import AbstractViewSet
from .serializers import BimaCoreSkillLevelSerializer
from .models import SkillLevel
class BimaCoreSkilllevelViewSet(AbstractViewSet):
    queryset = SkillLevel.objects.all()
    serializer_class = BimaCoreSkillLevelSerializer
    permission_classes = []
