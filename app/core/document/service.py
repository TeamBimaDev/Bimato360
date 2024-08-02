import logging
from enum import Enum

from common.converters.default_converters import str_to_bool
from common.enums.file_type import FileTypeCompany
from common.enums.file_type import FileTypeUser
from common.service.file_service import resize_image as image_resizer

logger = logging.getLogger(__name__)


class FileType(Enum):
    COMPANY_LOGO = (200, 100)
    USER_PROFILE_PICTURE = (186, 186)


def resize_image(document_data, file, file_content_type):
    if file_content_type.startswith('image/'):
        try:
            dimensions = get_dimensions_for_file_type(document_data)
            if dimensions is not None:
                file = image_resizer(file, *dimensions)
        except Exception as ex:
            logger.error(f"error occurred when resizing the image {ex}")
            pass

    return file


def get_dimensions_for_file_type(document_data):
    file_type = document_data['file_type']
    for type in FileType:
        if file_type == type.name:
            return type.value
    return None


def get_supported_type_for_resize(document_data):
    return document_data['file_type'] == FileTypeCompany.COMPANY_LOGO.name or \
        document_data['file_type'] == FileTypeUser.USER_PROFILE_PICTURE.name


def verify_is_favorite_item_exist(document_data, existing_docs):
    if (
            get_supported_type_for_resize(document_data)
            and str_to_bool(document_data.get('is_favorite', False))
            and existing_docs is not None
    ):
        existing_docs.update(is_favorite=False)
