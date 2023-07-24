from django.db.models.signals import post_save
from django.dispatch import receiver

from app.core.bank.models import BimaCoreBank


@receiver(post_save, sender=BimaCoreBank)
def create_addresses(sender, instance, new_creation, **kwargs):
    if new_creation:
        pass
