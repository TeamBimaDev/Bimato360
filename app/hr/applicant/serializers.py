from .models import BimaHrApplicant
from core.abstract.serializers import AbstractSerializer

class BimaHrApplicantSerializer(AbstractSerializer):
    class Meta:
        model = BimaHrApplicant
        fields = '__all__'