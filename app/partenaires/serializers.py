from core.abstract.serializers import AbstractSerializer
from .models import Bimapartenaires


class BimapartenairesSerializer(AbstractSerializer):
    class Meta:
        model = Bimapartenaires
        fields = '__all__'