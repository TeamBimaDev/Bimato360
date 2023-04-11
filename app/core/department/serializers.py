from core.abstract.serializers import AbstractSerializer
from .models import BimaCoreDepartment

class BimaCoreDepartmentSerializer(AbstractSerializer):
    class Meta:
        model = BimaCoreDepartment
        fields = '__all__'