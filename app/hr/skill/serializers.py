from core.abstract.serializers import AbstractSerializer
from .models import BimaHrSkill

class BimaHrSkillSerializer(AbstractSerializer):
    class Meta:
        model = BimaHrSkill
        fields = '__all__'
