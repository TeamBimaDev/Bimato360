from core.contact.models import BimaCoreContact
from django.contrib.contenttypes.models import ContentType


class BimaErpPartnerService:
    @staticmethod
    def get_partner_contacts(partner):
        return BimaCoreContact.objects.filter(
            parent_type=ContentType.objects.get_for_model(partner),
            parent_id=partner.id
        )
