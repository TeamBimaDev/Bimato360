import logging
from rest_framework.views import exception_handler
from django.http import JsonResponse
from requests import ConnectionError
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.exceptions import ValidationError, AuthenticationFailed, PermissionDenied
from django.core.exceptions import ObjectDoesNotExist


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    logger = logging.getLogger(__name__)
    print("test")
    print(response)
    print("done")
    print(context)

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
        'code': response_status
    }

    logger.error(f'An error occurred: {response_data}')

    response = JsonResponse(response_data, status=response_status)

    return response
