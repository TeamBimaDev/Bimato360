from core.abstract.views import AbstractViewSet
from .serializers import BimaCoreSkillCategorySerializer
from .models import SkillCategory





class BimaCoreSkillCategorViewSet(AbstractViewSet):
    queryset = SkillCategory.objects.all()
    serializer_class = BimaCoreSkillCategorySerializer
    permission_classes = []