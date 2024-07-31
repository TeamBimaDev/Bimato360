<<<<<<< HEAD
from enum import Enum

from django.utils.translation import gettext_lazy as _


class BimaHrInterviewStatus(Enum):
    COMPLETED = _('Completed')
    EXPIRED = _('Expired')
    PLANNED = _('Planned')


class BimaHrInterviewType(Enum):
    TECHNICAL = _('Technical')
    HR = _('Hr')
    
    
    
class BimaHrInterviewDueDate(Enum):
    One_Day   = _('1 Day')  
    Two_Day   = _('2 Day')
    Three_Day = _('3 Day')
    
class BimaHrInterviewTime(Enum):
    Half_hour = _('30 min')
    One_hour = _('1 h')
    One_hour_half = _('1h:30min') 
    
def get_interview_time_choices():
    return [(its.name, its.value) for its in BimaHrInterviewTime]
    
def get_interview_due_data_choices():   
    return [(its.name, its.value) for its in BimaHrInterviewDueDate]

def get_interview_status_choices():
    return [(its.name, its.value) for its in BimaHrInterviewStatus]


def get_interview_type_choices():
    return [(cp.name, cp.value) for cp in BimaHrInterviewType]
=======
from enum import Enum

from django.utils.translation import gettext_lazy as _


class BimaHrInterviewStatus(Enum):
    COMPLETED = _('Completed')
    EXPIRED = _('Expired')
    PLANNED = _('Planned')



class BimaHrInterviewType(Enum):
    TECHNICAL = _('Technical')
    HR = _('Hr')

class BimaHrInterviewDueDate(Enum):
    One_Day= _('1 Day')
    Two_Day= _('2 Day')
    Three_Day = _('3 Day')

class BimaHrInterviewTime(Enum):
    Half_hour = _("30 min")
    One_hour = _("1 h")
    One_hour_half = _('1h:30min')

def get_interview_status_choices():
    return [(its.name, its.value) for its in BimaHrInterviewStatus]


def get_interview_type_choices():
    return [(cp.name, cp.value) for cp in BimaHrInterviewType]

def get_interview_due_data_choices():
    return [(its.name, its.value) for its in BimaHrInterviewDueDate]

def get_interview_time_choices():
    return [(its.name, its.value) for its in BimaHrInterviewTime]
>>>>>>> origin/ma-branch
