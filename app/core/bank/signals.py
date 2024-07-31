<<<<<<< HEAD
from django.dispatch import receiver, Signal
from django.db import transaction
from core.address.models import create_address_from_parent_entity

post_create_bank = Signal()


@receiver(post_create_bank)
@transaction.atomic
def create_bank_related_entities(sender, instance, address_data, **kwargs):
    if address_data:
        create_addresses(address_data, instance)


def create_addresses(addresses_data, partner):
    create_address_from_parent_entity(addresses_data, partner)
=======
from django.dispatch import receiver, Signal
from django.db import transaction
from core.address.models import create_address_from_parent_entity

post_create_bank = Signal()


@receiver(post_create_bank)
@transaction.atomic
def create_bank_related_entities(sender, instance, address_data, **kwargs):
    if address_data:
        create_addresses(address_data, instance)


def create_addresses(addresses_data, partner):
    create_address_from_parent_entity(addresses_data, partner)
>>>>>>> origin/ma-branch
