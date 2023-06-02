from enum import Enum


class PartnerType(Enum):
    INDIVIDUAL = 'Individual'
    COMPANY = 'Company'


def get_partner_type_choices():
    return [(pt.name, pt.value) for pt in PartnerType]
