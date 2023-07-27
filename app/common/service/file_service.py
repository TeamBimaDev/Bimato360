import os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _


def resize_image(image, width, height):
    img = Image.open(image)
    img.thumbnail((width, height), Image.LANCZOS)

    temp_file = BytesIO()
    img.save(temp_file, format=img.format or 'PNG')
    temp_file.seek(0)

    return ContentFile(temp_file.read(), name=image.name)


def check_csv_file(csv_file):
    if csv_file is None:
        return {'error', _("unable to read the file")}

    file_content_type = csv_file.content_type
    file_extension = os.path.splitext(csv_file.name)[1].lower()
    if file_content_type != "text/csv" and file_extension != ".csv":
        return {'error', _('Incorrect file type')}

    return {'success', 'File is good'}
