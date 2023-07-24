from enum import Enum
from django.utils.translation import gettext_lazy as _


class FileType(Enum):
    pass


class FileTypePartner(FileType):
    PARTNER_PICTURE = _('PARTNER_PICTURE')
    PARTNER_PRIVATE_DOCUMENT = _('PARTNER_PRIVATE_DOCUMENT')
    PARTNER_CIRET_DOCUMENT = _('PARTNER_CIRET_DOCUMENT')


class FileTypeCompany(FileType):
    COMPANY_LOGO = _('Logo')
    COMPANY_DOCUMENT = _('Documents')


class FileTypeBank(FileType):
    EMPLOYEE_CV = _('EMPLOYEE_CV')
    EMPLOYEE_RESUME = _('EMPLOYEE_RESUME')
    EMPLOYEE_DRIVER_LICENCE = _('EMPLOYEE_DRIVER_LICENCE')
    EMPLOYEE_PICTURE = _('EMPLOYEE_PICTURE')


class FileTypeUser(FileType):
    USER_PROFILE_PICTURE = _('USER_PROFILE_PICTURE')
    USER_OTHER = _('USER_OTHER')


def get_file_type_choices():
    choices = []
    for enum_class in FileType.__subclasses__():
        choices += [(choice.name, choice.value) for choice in enum_class]
    return choices


def return_list_file_type_partner():
    return [(file_type.name, file_type.value) for file_type in FileTypePartner]


def return_list_file_type_company():
    return [(file_type.name, file_type.value) for file_type in FileTypeCompany]


def return_list_file_type_user():
    return [(file_type.name, file_type.value) for file_type in FileTypeUser]
