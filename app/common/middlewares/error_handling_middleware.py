import logging
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError, \
    AuthenticationFailed, \
    PermissionDenied
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
class ErrorHandlingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        error_message = str(exception)

        if isinstance(exception, (ValidationError,)):
            response_status = HTTP_400_BAD_REQUEST
        elif isinstance(exception, (AuthenticationFailed,)):
            response_status = HTTP_401_UNAUTHORIZED
        elif isinstance(exception, (PermissionDenied,)):
            response_status = HTTP_403_FORBIDDEN
        elif isinstance(exception, (ObjectDoesNotExist,)):
            response_status = HTTP_404_NOT_FOUND
        else:
            response_status = HTTP_500_INTERNAL_SERVER_ERROR

        response_data = {
            'succeeded': False,
            'message': error_message,
            'code': response_status
        }

        self.logger.error(f'An error occurred: {response_data}')

        response = JsonResponse(response_data, status=response_status)

        return response
