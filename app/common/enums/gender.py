<<<<<<< HEAD
from enum import Enum
from django.utils.translation import gettext_lazy as _


class Gender(Enum):
    MALE = _('Male')
    FEMALE = _('Female')


def get_gender_choices():
    return [(gender.name, gender.value) for gender in Gender]
=======
from enum import Enum
from django.utils.translation import gettext_lazy as _


class Gender(Enum):
    MALE = _('Male')
    FEMALE = _('Female')


def get_gender_choices():
    return [(gender.name, gender.value) for gender in Gender]
>>>>>>> origin/ma-branch
