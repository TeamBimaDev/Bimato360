from core.abstract.serializers import AbstractSerializer
from company.models import BimaCompany


class BimaCompanySerializer(AbstractSerializer):
    class Meta:
        model = BimaCompany
        fields = '__all__'
