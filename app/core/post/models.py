from core.abstract.models import AbstractModel
from django.db import models
from core.department.models import BimaCoreDepartment
class BimaCorePost(AbstractModel ):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)
    responsibilities= models.TextField(blank=True, null=True)
    department_id = models.ForeignKey(BimaCoreDepartment, on_delete=models.CASCADE, null=True)


    def __str__(self) -> str:
        return f"{self.id,self.name , self.description, self.responsibilities ,self.requirements }"
    class Meta:
        ordering = ['name']
        permissions = []