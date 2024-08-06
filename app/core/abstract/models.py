
import uuid
from logging import getLogger
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ValidationError

logger = getLogger(__name__)


class AbstractManager(models.Manager):
    def get_object_by_public_id(self, public_id):
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            raise Http404


class AbstractModel(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True,
                                 default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = AbstractManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.pk and 'active' in self.__dict__ and not self.active:
            for rel in self._meta.related_objects:
                if rel.get_accessor_name() is not None:
                    try:
                        related = getattr(self, rel.get_accessor_name())
                        if hasattr(related, 'all'):
                            if related.all().exists():
                                raise ValidationError({'Active': _("L'élément est utilisé, impossible de changer vers "
                                                                   "désactiver")})
                        else:
                            raise ValidationError({'Active': _("L'élément est utilisé, impossible de changer vers "
                                                               "désactiver")})
                    except ObjectDoesNotExist:
                        pass

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        try:
            super().delete(*args, **kwargs)
        except ProtectedError:
            raise ValidationError({"Delete": _("Impossible de supprimer cet élément car il est lié à un autre élément.")})

