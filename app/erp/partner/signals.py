from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver, Signal
from django.db import transaction
from django.shortcuts import get_object_or_404

from core.address.models import BimaCoreAddress
from core.contact.models import BimaCoreContact
from core.country.models import BimaCoreCountry
from core.state.models import BimaCoreState
from erp.partner.models import BimaErpPartner

post_create_partner = Signal()


@receiver(post_create_partner)
@transaction.atomic
def create_partner_related_entities(sender, instance, address_data, contact_data, document_data, **kwargs):
    if address_data:
        create_addresses(address_data, instance)

    if contact_data:
        create_contacts(contact_data, instance)

    if document_data:
        create_documents(document_data, instance)


def create_addresses(addresses_data, partner):
    for address_data in addresses_data:
        country = get_object_or_404(BimaCoreCountry, public_id=address_data['country'])
        state = get_object_or_404(BimaCoreState, public_id=address_data['state'])

        BimaCoreAddress.objects.create(
            number=address_data['number'],
            street=address_data['street'],
            street2=address_data['street2'],
            zip=address_data['zip'],
            city=address_data['city'],
            contact_name=address_data['contact_name'],
            contact_phone=address_data['contact_phone'],
            contact_email=address_data['contact_email'],
            can_send_bill=address_data['can_send_bill'],
            can_deliver=address_data['can_deliver'],
            latitude=address_data['latitude'],
            longitude=address_data['longitude'],
            note=address_data['note'],
            state_id=state.id,
            country_id=country.id,
            parent_type=ContentType.objects.get_for_model(BimaErpPartner),
            parent_id=partner.id,
        )


def create_contacts(contacts_data, partner):
    for contact_data in contacts_data:
        BimaCoreContact.objects.create(
            name=contact_data['name'],
            position=contact_data['position'],
            department=contact_data['department'],
            email=contact_data['email'],
            fax=contact_data['fax'],
            mobile=contact_data['mobile'],
            phone=contact_data['phone'],
            gender=contact_data['gender'],
            parent_type=ContentType.objects.get_for_model(BimaErpPartner),
            parent_id=partner.id,
        )


def create_documents(documents_data, partner):
    pass
