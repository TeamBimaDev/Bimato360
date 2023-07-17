from enum import Enum

from common.enums.file_type import FileTypeCompany
from common.service.file_service import resize_image
from common.enums.file_type import FileTypeUser


class FileType(Enum):
    COMPANY_LOGO = (200, 100)
    USER_PROFILE_PICTURE = (186, 186)


def resize_image(document_data, file, file_content_type):
    if file_content_type.startswith('image/'):
        try:
            dimensions = get_dimensions_for_file_type(document_data)
            if dimensions is not None:
                file = resize_image(file, *dimensions)
        except Exception as e:
            print(f"Failed to resize the image. Error: {str(e)}")
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
            and document_data.get('is_favorite', False)
            and existing_docs is not None
    ):
        existing_docs.update(is_favorite=False)
