from core.abstract.serializers import AbstractSerializer
from .models import SkillLevel
class BimaCoreSkillLevelSerializer(AbstractSerializer):
    class Meta:
        model = SkillLevel
        fields = '__all__'
