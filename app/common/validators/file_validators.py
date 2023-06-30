from django.core.exceptions import ValidationError


def validate_file_size(value):
    file_size = value.size
    limit_mb = 5
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(f'Max file size is {limit_mb}MB')


def validate_file_extension(value):
    valid_extensions = ['xls', 'xlsx', 'png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx', 'ppt', 'pptx']
    ext = value.name.split('.')[-1]
    if ext not in valid_extensions:
        raise ValidationError(f'Invalid file extension, allowed extensions are {", ".join(valid_extensions)}')
