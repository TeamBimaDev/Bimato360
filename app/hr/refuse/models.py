from core.abstract.models import AbstractModel
from django.db import models
from hr.applicant.models import BimaHrApplicant
from core.post.models import BimaCorePost
class BimaHrRefuse(AbstractModel):
    raison = models.CharField(max_length=528, blank=False)
    date = models.DateTimeField()
    id_manager = models.IntegerField()
    applicant = models.ForeignKey(BimaHrApplicant, on_delete=models.PROTECT)
    poste = models.ForeignKey(BimaCorePost, on_delete=models.PROTECT)

    def __str__(self):
        return self.raison

    class Meta:
        ordering = ['raison']
        permissions = []



