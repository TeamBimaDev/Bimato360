from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import filters

from .base_filter import BaseFilter
from .pagination import DefaultPagination

from rest_framework.exceptions import ValidationError, AuthenticationFailed, PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


class AbstractViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = BaseFilter
    ordering_fields = ['updated', 'created']
    ordering = ['-updated']
    pagination_class = DefaultPagination

    def handle_exception(self, exc):
        if exc.status_code:
            error_status_code = exc.status_code
        else:
            if isinstance(exc, (ValidationError,)):
                error_status_code = HTTP_400_BAD_REQUEST
            elif isinstance(exc, (AuthenticationFailed,)):
                error_status_code = HTTP_401_UNAUTHORIZED
            elif isinstance(exc, (PermissionDenied,)):
                error_status_code = HTTP_403_FORBIDDEN
            elif isinstance(exc, (ObjectDoesNotExist,)):
                error_status_code = HTTP_404_NOT_FOUND
            else:
                error_status_code = HTTP_500_INTERNAL_SERVER_ERROR

        error_message = "A server error occurred"
        if len(exc.args[0]):
            error_message = exc.args[0]

        response = super().handle_exception(exc)

        # Customize the response format
        custom_response_data = {
            'succeeded': False,
            'message': format_error_message(error_message),
            'code': error_status_code,
            'data': None,
        }

        response.data = custom_response_data

        return response


def format_error_message(error_message):
    if not error_message:
        return ""

    if isinstance(error_message, str):
        return error_message

    if isinstance(error_message, dict):
        formatted_message = "\n"
        for field, errors in error_message.items():
            formatted_message += f"\t{field}: ["
            for error in errors:
                formatted_message += f"(string='{error}')"
                if error != errors[-1]:
                    formatted_message += ", "
            formatted_message += "],\n"

        return formatted_message
