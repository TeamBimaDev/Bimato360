from django.db import models
from core.abstract.models import AbstractModel
from core.poste.models import BimaCorePoste
from  hr.applicant.models import BimaHrApplicant
class BimaHrCondidatPoste(AbstractModel):
    expected_salary = models.FloatField()
    proposed_salary = models.FloatField()
    accepted_salary = models.FloatField()
    date = models.DateTimeField()
    id_candidat =  models.ManyToManyField(BimaHrApplicant ,related_name='condidat_postes')
    id_poste =  models.ManyToManyField(BimaCorePoste , related_name='condidat_postes')

    def __str__ (self) -> str:
        return self.name
