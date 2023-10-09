from enum import Enum

from django.utils.translation import gettext_lazy as _


class SeniorityType(Enum):
    JUNIOR = _('Junior')
    MID_LEVEL = _('Mid-level')
    SENIOR = _('Senior')
    EXECUTIVE = _('Executive')


class ContractType(Enum):
    CDD = _('CDD')
    CDI = _('CDI')
    CVP = _('CVP')
    INTERNSHIP = _('Internship')
    KARAMA = _('Karama')


class ContractStatus(Enum):
    ACTIVE = _('Active')
    SUSPENDED = _('Suspended')
    EXPIRED = _('Expired')
    TERMINATED = _('Terminated')


def get_seniority_choices():
    return [(seniority.name, seniority.value) for seniority in SeniorityType]


def get_contract_type_choices():
    return [(contract.name, contract.value) for contract in ContractType]


def get_contract_status_choices():
    return [(st.name, st.value) for st in ContractStatus]
