from core.abstract.views import AbstractViewSet

from .models import BimaHrSkill
from .serializers import BimaHrSkillSerializer


class BimaHrSkillViewSet(AbstractViewSet):
    queryset = BimaHrSkill.objects.all()
    serializer_class = BimaHrSkillSerializer
    permission_classes = []
