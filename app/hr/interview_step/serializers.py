from core.abstract.serializers import AbstractSerializer

from .models import BimaHrInterviewStep


class BimaHrInterviewStepSerializer(AbstractSerializer):
    class Meta:
        model = BimaHrInterviewStep
        fields = '__all__'
