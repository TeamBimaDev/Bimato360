from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


def resize_image(image, width, height):
    img = Image.open(image)
    img.thumbnail((width, height), Image.ANTIALIAS)

    temp_file = BytesIO()
    img.save(temp_file, format=img.format or 'PNG')
    temp_file.seek(0)

    return ContentFile(temp_file.read(), name=image.name)
