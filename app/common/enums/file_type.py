from enum import Enum


class FileType(Enum):
    pass


class FileTypePartner(FileType):
    PARTNER_PICTURE = 'PARTNER_PICTURE'
    PARTNER_PRIVATE_DOCUMENT = 'PARTNER_PRIVATE_DOCUMENT'
    PARTNER_CIRET_DOCUMENT = 'PARTNER_CIRET_DOCUMENT'


class FileTypeBank(Enum):
    EMPLOYEE_CV = 'EMPLOYEE_CV'
    EMPLOYEE_RESUME = 'EMPLOYEE_RESUME'
    EMPLOYEE_DRIVER_LICENCE = 'EMPLOYEE_DRIVER_LICENCE'
    EMPLOYEE_PICTURE = 'EMPLOYEE_PICTURE'


def get_file_type_choices():
    choices = []
    for enum_class in FileType.__subclasses__():
        choices += [(choice.name, choice.value) for choice in enum_class]
    return choices


def return_list_file_type_partner():
    return [(file_type.name, file_type.value) for file_type in FileTypePartner]
