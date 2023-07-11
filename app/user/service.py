from common.enums.file_type import FileTypeUser
from django.contrib.contenttypes.models import ContentType
from core.document.models import BimaCoreDocument


def get_favorite_user_profile_image(user):
    return BimaCoreDocument.objects.filter(
        parent_type=ContentType.objects.get_for_model(user),
        parent_id=user.id,
        file_type=FileTypeUser.USER_PROFILE_PICTURE.name,
        is_favorite=True
    ).first()
