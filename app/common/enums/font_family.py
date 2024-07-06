from enum import Enum


class FontFamilyEnum(Enum):
    ARIAL = 'Arial'
    TIMES_NEW_ROMAN = 'Times New Roman'
    HELVETICA = 'Helvetica'
    VERDANA = 'Verdana'
    COURIER_NEW = 'Courier New'
    OPEN_SANS = 'Open Sans'
    ROBOTO = 'Roboto'
    GEORGIA = 'Georgia'
    MONTSERRAT = 'Montserrat'
    LATO = 'Lato'


def get_font_family_list():
    return [(ff.value, ff.value) for ff in FontFamilyEnum]
