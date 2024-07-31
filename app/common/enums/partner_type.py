<<<<<<< HEAD
from enum import Enum
from django.utils.translation import gettext_lazy as _


class PartnerType(Enum):
    INDIVIDUAL = _('Individual')
    COMPANY = _('Company')


def get_partner_type_choices():
    return [(pt.name, pt.value) for pt in PartnerType]
=======
from enum import Enum
from django.utils.translation import gettext_lazy as _


class PartnerType(Enum):
    INDIVIDUAL = _('Individual')
    COMPANY = _('Company')


def get_partner_type_choices():
    return [(pt.name, pt.value) for pt in PartnerType]
>>>>>>> origin/ma-branch
