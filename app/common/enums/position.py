from enum import Enum

from django.utils.translation import gettext_lazy as _


class SeniorityType(Enum):
    JUNIOR = _('Junior')
    MID_LEVEL = _('Mid-level')
    SENIOR = _('Senior')
    EXECUTIVE = _('Executive')


class ContractType(Enum):
    CDI = _('CDI')
    CDD = _('CDD')
    APPRENTICESHIP = _('Apprenticeship')


def get_seniority_choices():
    return [(seniority.name, seniority.value) for seniority in SeniorityType]


def get_contract_type_choices():
    return [(contract.name, contract.value) for contract in ContractType]
