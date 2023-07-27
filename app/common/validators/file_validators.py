from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_file_size(value):
    file_size = value.size
    limit_mb = 5
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(_(f'La taille maximale du fichier est de {limit_mb}MB'))


def validate_file_extension(value):
    valid_extensions = ['xls', 'xlsx', 'png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx', 'ppt', 'pptx']
    ext = value.name.split('.')[-1]
    if ext not in valid_extensions:
        raise ValidationError(
            _(f'Extension de fichier non valide, les extensions autorisées sont {", ".join(valid_extensions)}'))


def validate_file_extension_is_image(value):
    valid_extensions = ['png', 'jpg', 'jpeg']
    ext = value.name.split('.')[-1]
    if ext not in valid_extensions:
        raise ValidationError(
            _(f'Extension de fichier non valide, les extensions autorisées sont {", ".join(valid_extensions)}'))
