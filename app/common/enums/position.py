from enum import Enum

from django.utils.translation import gettext_lazy as _


class SeniorityType(Enum):
    JUNIOR = _('Junior')
    MID_LEVEL = _('Mid-level')
    SENIOR = _('Senior')
    EXECUTIVE = _('Executive')

class ToneType(Enum):
    Causal = _('Causal')
    Friendly = _('Friendly')
    Professional = _('Professional')
    Formal = _('Formal')

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
    
    
class offreStatus(Enum):
    Published = _('Published')
    Unpublished = _('Unpublished')
      
          

class TerminationReason(Enum):
    MUTUAL_TERMINATION = _('Mutual Termination')
    DISMISSAL = _('Dismissal')
    RESIGNATION = _('Resignation')
    CONTRACT_TERMINATION = _('Contract Termination')
    OTHER = _('Other')


class SuspensionReason(Enum):
    SICK_LEAVE = _('Sick Leave')
    MATERNITY_LEAVE = _('Maternity Leave')
    PROFESSIONAL_TRAINING = _('Professional Training')
    WORK_ACCIDENT = _('Work Accident')
    DISCIPLINARY_SUSPENSION = _('Disciplinary Suspension')
    OTHER = _('Other')

class PositionStatusType(Enum):
    ACTIVE = _('Active')
    CLOSED = _('Closed')

def get_seniority_choices():
    return [(seniority.name, seniority.value) for seniority in SeniorityType]

def get_tone_choices():
    return [(tone.name, tone.value) for tone in ToneType]


def get_contract_type_choices():
    return [(contract.name, contract.value) for contract in ContractType]


def get_contract_status_choices():
    return [(st.name, st.value) for st in ContractStatus]


def get_termination_reason_choices():
    return [(reason.name, reason.value) for reason in TerminationReason]


def get_suspension_reason_choices():
    return [(reason.name, reason.value) for reason in SuspensionReason]

def get_position_status_choices():
    return [(ps.name, ps.value) for ps in PositionStatusType]


def get_offre_status_choices():
    return [(offre.name, offre.value) for offre in offreStatus]