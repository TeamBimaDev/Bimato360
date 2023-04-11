from core.abstract.models import AbstractModel
from django.db import models
from hr.applicant.models import BimaHrApplicant
from core.poste.models import BimaCorePoste
class BimaHrRefuse(AbstractModel):
    raison = models.CharField(max_length=528, blank=False)
    date = models.DateTimeField()
    id_manager = models.IntegerField()
    applicant = models.ForeignKey(BimaHrApplicant, on_delete=models.PROTECT)
    poste = models.ForeignKey(BimaCorePoste, on_delete=models.PROTECT)

    def __str__(self):
        return self.raison

    class Meta:
        ordering = ['raison']
        permissions = []



