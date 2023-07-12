from common.enums.file_type import FileTypeUser
from django.contrib.contenttypes.models import ContentType
from core.document.models import BimaCoreDocument


def get_favorite_user_profile_image(user):
    favorite_image = BimaCoreDocument.objects.filter(
        parent_type=ContentType.objects.get_for_model(user),
        parent_id=user.id,
        file_type=FileTypeUser.USER_PROFILE_PICTURE.name,
        is_favorite=True
    ).first()

    if favorite_image is not None:
        return favorite_image

    return BimaCoreDocument.objects.filter(
        parent_type=ContentType.objects.get_for_model(user),
        parent_id=user.id,
        file_type=FileTypeUser.USER_PROFILE_PICTURE.name,
    ).order_by('-date_file').first()
