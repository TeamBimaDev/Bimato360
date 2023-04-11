from hr.interview.models import BimaHrInterview
from core.abstract.serializers import AbstractSerializer


class BimaHrInterviewSerializer(AbstractSerializer):
    class Meta:
        model = BimaHrInterview
        fields = '__all__'