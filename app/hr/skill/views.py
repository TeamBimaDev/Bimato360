from core.abstract.views import AbstractViewSet

from .serializers import  BimaHrSkillSerializer
from .models import BimaHrSkill

class BimaCoreSkillViewSet(AbstractViewSet):
    queryset = BimaHrSkill.objects.all()
    serializer_class = BimaHrSkillSerializer
    permission_classes = []





