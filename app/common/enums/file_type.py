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


class FileTypeEmployee(FileType):
    EMPLOYEE_CV = _('EMPLOYEE_CV')
    EMPLOYEE_RESUME = _('EMPLOYEE_RESUME')
    EMPLOYEE_DRIVER_LICENCE = _('EMPLOYEE_DRIVER_LICENCE')
    EMPLOYEE_PICTURE = _('EMPLOYEE_PICTURE')
    EMPLOYEE_CONTRACT = _('EMPLOYEE_CONTRACT')


class FileTypeUser(FileType):
    USER_PROFILE_PICTURE = _('USER_PROFILE_PICTURE')
    USER_OTHER = _('USER_OTHER')


class FilePurchaseDocument(FileType):
    SELLER_PURCHASE_QUOTE_DOCUMENT = _('SELLER_PURCHASE_QUOTE_DOCUMENT')
    SELLER_PURCHASE_ORDER_DOCUMENT = _('SELLER_PURCHASE_ORDER_DOCUMENT')
    SELLER_PURCHASE_INVOICE_DOCUMENT = _('SELLER_PURCHASE_INVOICE_DOCUMENT')


class FileContract(FileType):
    CONTRACT_MAIN = _('CONTRACT_MAIN')
    CONTRACT_RENEW = _('CONTRACT_RENEW')
    CONTRACT_AMENDMENT = _('CONTRACT_AMENDMENT')
    RESIGNATION = _('RESIGNATION')

class FileTypeCandidat(FileType):
    CANDIDAT_CV = _('CANDIDAT_CV')
    CANDIDAT_RESUME = _('CANDIDAT_RESUME')
    CANDIDAT_PICTURE = _('CANDIDAT_PICTURE')
    CANDIDAT_OTHER = _('CANDIDAT_OTHER')  

def return_list_file_candidat():
    return [(cand.name, cand.value) for cand in FileTypeCandidat]


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


def return_list_file_purchase_document():
    return [(file_type.name, file_type.value) for file_type in FilePurchaseDocument]


def return_list_file_employee():
    return [(emp.name, emp.value) for emp in FileTypeEmployee]


def return_list_file_contract():
    return [(emp.name, emp.value) for emp in FileContract]
