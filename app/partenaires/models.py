from django.db import models

# Create your models here.
from core.abstract.models import AbstractModel
class Bimapartenaires(AbstractModel):
    name_supplier=models.BooleanField()
    name_customer =models.BooleanField()
    Email = models.EmailField()
    Phone = models.CharField()
    Fax= models.CharField()



