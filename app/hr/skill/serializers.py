from core.abstract.serializers import AbstractSerializer
from .models import BimaHrSkill
from hr.skill_category.serializers import  BimaCoreSkillCategorySerializer
from hr.applicant.serializers import BimaHrApplicantSerializer

class BimaHrSkillSerializer(AbstractSerializer):

    class Meta:
        model = BimaHrSkill
        fields = '__all__'
