from django.db import models


class GlobalPermission(models.Model):
    """
    This model is used for the sole purpose of creating global permissions
    that are not associated with a specific model.
    """
    pass
