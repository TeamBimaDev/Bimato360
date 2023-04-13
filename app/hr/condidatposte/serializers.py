from core.abstract.serializers import AbstractSerializer
from .models import BimaHrCondidatPoste

class BimaHrCondidatPosteSerializer(AbstractSerializer):
    class Meta:
        model = BimaHrCondidatPoste
        fields = ['expected_salary','proposed_salary' ,'accepted_salary','date','id_candidat','id_poste'
                                                                                              '']
