from django.db import models
from core.abstract.models import AbstractModel
from core.poste.models import BimaCorePoste
from  hr.applicant.models import BimaHrApplicant
class BimaHrCondidatPoste(AbstractModel):
    expected_salary = models.FloatField(blank=True, null=True, default=None)
    proposed_salary = models.FloatField(blank=True, null=True, default=None)
    accepted_salary = models.FloatField(blank=True, null=True, default=None)
    date = models.DateTimeField(auto_now_add=True)
    id_candidat =  models.ManyToManyField(BimaHrApplicant ,related_name='condidat_postes',null=True, blank=True)
    id_poste =  models.ManyToManyField(BimaCorePoste , related_name='condidat_postes',null=True, blank=True)

    def __str__ (self) -> str:
        return self.name
