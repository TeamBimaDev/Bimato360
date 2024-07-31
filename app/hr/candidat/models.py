<<<<<<< HEAD
from django.db import models
from core.abstract.models import AbstractModel
from hr.models import BimaHrPerson
from simple_history.models import HistoricalRecords
from django.utils import timezone

class BimaHrCandidat(BimaHrPerson):
    availability_days = models.IntegerField()
    message = models.TextField(max_length=256)
    
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.first_name, self.last_name}"

    class Meta:
        ordering = ['first_name']
        permissions = []
        default_permissions = ()

=======
from django.db import models
from core.abstract.models import AbstractModel
from hr.models import BimaHrPerson
from simple_history.models import HistoricalRecords
from django.utils import timezone

class BimaHrCandidat(BimaHrPerson):
    availability_days = models.IntegerField()
    message = models.TextField(max_length=256)
    
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.first_name, self.last_name}"

    class Meta:
        ordering = ['first_name']
        permissions = []
        default_permissions = ()

>>>>>>> origin/ma-branch
