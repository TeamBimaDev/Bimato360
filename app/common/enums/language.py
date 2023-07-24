from django.utils.translation import gettext_lazy as _
from django.db import models


class LanguageEnum(models.TextChoices):
    ENGLISH = 'EN', _('English')
    FRENCH = 'FR', _('French')
