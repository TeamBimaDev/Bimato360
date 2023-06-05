from django.dispatch import receiver, Signal
from django.db import transaction

from core.address.models import create_address_from_parent_entity
from core.contact.models import create_contact_from_parent_entity
from core.document.models import create_document_from_parent_entity
from core.entity_tag.models import create_entity_tag_from_parent_entity

post_create_partner = Signal()


@receiver(post_create_partner)
@transaction.atomic
def create_partner_related_entities(sender, instance, address_data, contact_data, document_data, tag_data, **kwargs):
    if address_data:
        create_addresses(address_data, instance)

    if contact_data:
        create_contacts(contact_data, instance)

    # if document_data:
    #     create_documents(document_data, instance)

    if tag_data:
        create_tags(tag_data, instance)


def create_addresses(addresses_data, partner):
    create_address_from_parent_entity(addresses_data, partner)


def create_contacts(contacts_data, partner):
    create_contact_from_parent_entity(contacts_data, partner)


def create_documents(documents_data, partner):
    create_document_from_parent_entity(documents_data, partner)


def create_tags(tags_data, partner):
    create_entity_tag_from_parent_entity(tags_data, partner)
