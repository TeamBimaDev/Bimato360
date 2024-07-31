<<<<<<< HEAD
from django.db import models

from core.abstract.models import AbstractModel


class BimaErpUnitOfMeasure(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    active = models.BooleanField(default=True)
    is_default_for_service_product = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()

    def save(self, *args, **kwargs):
        if self.is_default_for_service_product:
            BimaErpUnitOfMeasure.objects.filter(is_default_for_service_product=True).\
                update(is_default_for_service_product=False)
        super(BimaErpUnitOfMeasure, self).save(*args, **kwargs)
=======
from django.db import models

from core.abstract.models import AbstractModel


class BimaErpUnitOfMeasure(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    active = models.BooleanField(default=True)
    is_default_for_service_product = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()

    def save(self, *args, **kwargs):
        if self.is_default_for_service_product:
            BimaErpUnitOfMeasure.objects.filter(is_default_for_service_product=True).\
                update(is_default_for_service_product=False)
        super(BimaErpUnitOfMeasure, self).save(*args, **kwargs)
>>>>>>> origin/ma-branch
