<<<<<<< HEAD
import binascii
from datetime import timedelta

from common.enums.file_type import FileTypeUser
from core.document.models import BimaCoreDocument
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from rest_framework import status

from .models import User


def get_favorite_user_profile_image(user):
    favorite_image = BimaCoreDocument.objects.filter(
        parent_type=ContentType.objects.get_for_model(user),
        parent_id=user.id,
        file_type=FileTypeUser.USER_PROFILE_PICTURE.name,
        is_favorite=True,
    ).first()

    if favorite_image is not None:
        return favorite_image

    return (
        BimaCoreDocument.objects.filter(
            parent_type=ContentType.objects.get_for_model(user),
            parent_id=user.id,
            file_type=FileTypeUser.USER_PROFILE_PICTURE.name,
        )
        .order_by("-date_file")
        .first()
    )


def verify_user_credential_when_change_password(uidb64, token, public_id):
    if uidb64 is None or token is None or public_id is None:
        return {"detail": _("Missing parameters.")}, status.HTTP_400_BAD_REQUEST

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
    except (ValueError, binascii.Error):
        return {
            "detail": _("Unable to identify credential")
        }, status.HTTP_400_BAD_REQUEST

    try:
        user = User.objects.get(public_id=public_id)
    except User.DoesNotExist:
        return {"detail": _("Unable to identify credential")}, status.HTTP_404_NOT_FOUND

    if uid != str(user.pk):
        return {
            "detail": _("Unable to identify credential")
        }, status.HTTP_400_BAD_REQUEST

    if user.reset_password_token != token:
        return {
            "detail": _("Unable to identify credential")
        }, status.HTTP_400_BAD_REQUEST

    if (
        user.reset_password_token is None
        or user.reset_password_uid is None
        or user.reset_password_time is None
    ):
        return {"detail": _("User has been activated")}, status.HTTP_400_BAD_REQUEST

    if timezone.now() - user.reset_password_time > timedelta(hours=24):
        return {
            "detail": _("Your token has expired please contact the administrator")
        }, status.HTTP_400_BAD_REQUEST

    if user.reset_password_token != token:
        return {
            "detail": _("Unable to identify credential")
        }, status.HTTP_400_BAD_REQUEST

    return {"detail": "Valid token."}, status.HTTP_200_OK
=======
import binascii
from datetime import timedelta

from common.enums.file_type import FileTypeUser
from core.document.models import BimaCoreDocument
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from rest_framework import status

from .models import User


def get_favorite_user_profile_image(user):
    favorite_image = BimaCoreDocument.objects.filter(
        parent_type=ContentType.objects.get_for_model(user),
        parent_id=user.id,
        file_type=FileTypeUser.USER_PROFILE_PICTURE.name,
        is_favorite=True,
    ).first()

    if favorite_image is not None:
        return favorite_image

    return (
        BimaCoreDocument.objects.filter(
            parent_type=ContentType.objects.get_for_model(user),
            parent_id=user.id,
            file_type=FileTypeUser.USER_PROFILE_PICTURE.name,
        )
        .order_by("-date_file")
        .first()
    )


def verify_user_credential_when_change_password(uidb64, token, public_id):
    if uidb64 is None or token is None or public_id is None:
        return {"detail": _("Missing parameters.")}, status.HTTP_400_BAD_REQUEST

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
    except (ValueError, binascii.Error):
        return {
            "detail": _("Unable to identify credential")
        }, status.HTTP_400_BAD_REQUEST

    try:
        user = User.objects.get(public_id=public_id)
    except User.DoesNotExist:
        return {"detail": _("Unable to identify credential")}, status.HTTP_404_NOT_FOUND

    if uid != str(user.pk):
        return {
            "detail": _("Unable to identify credential")
        }, status.HTTP_400_BAD_REQUEST

    if user.reset_password_token != token:
        return {
            "detail": _("Unable to identify credential")
        }, status.HTTP_400_BAD_REQUEST

    if (
        user.reset_password_token is None
        or user.reset_password_uid is None
        or user.reset_password_time is None
    ):
        return {"detail": _("User has been activated")}, status.HTTP_400_BAD_REQUEST

    if timezone.now() - user.reset_password_time > timedelta(hours=24):
        return {
            "detail": _("Your token has expired please contact the administrator")
        }, status.HTTP_400_BAD_REQUEST

    if user.reset_password_token != token:
        return {
            "detail": _("Unable to identify credential")
        }, status.HTTP_400_BAD_REQUEST

    return {"detail": "Valid token."}, status.HTTP_200_OK
>>>>>>> origin/ma-branch
