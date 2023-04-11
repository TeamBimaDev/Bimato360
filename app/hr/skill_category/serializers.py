from core.abstract.serializers import AbstractSerializer
from .models import SkillCategory

class BimaCoreSkillCategorySerializer(AbstractSerializer):
    class Meta:
        model = SkillCategory
        fields = '__all__'