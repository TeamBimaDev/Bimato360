import logging

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.exceptions import ValidationError, \
    AuthenticationFailed, \
    PermissionDenied
from django.core.exceptions import ObjectDoesNotExist


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    logger = logging.getLogger(__name__)

    error_message = str(exc)

    if isinstance(exc, (ValidationError,)):
        response_status = HTTP_400_BAD_REQUEST
    elif isinstance(exc, (AuthenticationFailed,)):
        response_status = HTTP_401_UNAUTHORIZED
    elif isinstance(exc, (PermissionDenied,)):
        response_status = HTTP_403_FORBIDDEN
    elif isinstance(exc, (ObjectDoesNotExist,)):
        response_status = HTTP_404_NOT_FOUND
    else:
        response_status = HTTP_500_INTERNAL_SERVER_ERROR

    response_data = {
        'succeeded': False,
        'message': error_message,
        'code': response_status,
        'data': None
    }

    logger.error(f'An error occurred: {response_data}')

    response = Response(response_data, status=response_status)

    return response
