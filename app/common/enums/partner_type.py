from enum import Enum


class PartnerType(Enum):
    INDIVIDUAL = 'Individual'
    COMPANY = 'Company'


def get_partner_type_choices():
    return [(partner_type.name, partner_type.value) for partner_type in PartnerType]
