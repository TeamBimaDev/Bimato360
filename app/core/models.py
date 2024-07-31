<<<<<<< HEAD
from django.db import models


class GlobalPermission(models.Model):
    """
    This model is used for the sole purpose of creating global permissions
    that are not associated with a specific model.
    """

    class Meta:
        default_permissions = ()
=======
from django.db import models


class GlobalPermission(models.Model):
    """
    This model is used for the sole purpose of creating global permissions
    that are not associated with a specific model.
    """

    class Meta:
        default_permissions = ()
>>>>>>> origin/ma-branch
