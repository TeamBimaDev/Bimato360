from logging import getLogger

from django.http import Http404
from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.exceptions import (
    ValidationError,
    AuthenticationFailed,
    PermissionDenied,
    NotAuthenticated,
    NotFound,
    MethodNotAllowed,
    NotAcceptable,
    UnsupportedMediaType,
    ParseError,
    APIException,
    Throttled
)
from django.core.exceptions import ObjectDoesNotExist, BadRequest
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    HTTP_429_TOO_MANY_REQUESTS,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from .base_filter import BaseFilter
from .pagination import DefaultPagination
from django.utils.translation import gettext_lazy as _

logger = getLogger(__name__)

EXCEPTIONS_MAP = {
    ValidationError: {
        'status_code': HTTP_400_BAD_REQUEST,
        'message': _("Invalid input"),
    },
    BadRequest: {
        'status_code': HTTP_400_BAD_REQUEST,
        'message': _("Bad request"),
    },
    APIException: {
        'status_code': HTTP_400_BAD_REQUEST,
        'message': _("API exception occurred"),
    },
    ParseError: {
        'status_code': HTTP_400_BAD_REQUEST,
        'message': _("Malformed request"),
    },
    AuthenticationFailed: {
        'status_code': HTTP_401_UNAUTHORIZED,
        'message': _("Authentication failed"),
    },
    NotAuthenticated: {
        'status_code': HTTP_401_UNAUTHORIZED,
        'message': _("Not authenticated"),
    },
    PermissionDenied: {
        'status_code': HTTP_403_FORBIDDEN,
        'message': _("Permission denied"),
    },
    NotFound: {
        'status_code': HTTP_404_NOT_FOUND,
        'message': _("Resource not found"),
    },
    ObjectDoesNotExist: {
        'status_code': HTTP_404_NOT_FOUND,
        'message': _("Resource does not exist"),
    },
    MethodNotAllowed: {
        'status_code': HTTP_405_METHOD_NOT_ALLOWED,
        'message': _("Method not allowed"),
    },
    NotAcceptable: {
        'status_code': HTTP_406_NOT_ACCEPTABLE,
        'message': _("Request not acceptable"),
    },
    UnsupportedMediaType: {
        'status_code': HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        'message': _("Unsupported media type"),
    },
    Throttled: {
        'status_code': HTTP_429_TOO_MANY_REQUESTS,
        'message': _("Too many requests"),
    },
    Http404: {
        'status_code': HTTP_404_NOT_FOUND,
        'message': _("Unable to get the item"),
    }
}


class AbstractViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = BaseFilter
    ordering_fields = ['updated', 'created']
    ordering = ['name']
    pagination_class = DefaultPagination

    def get_error_message(self, exc):
        if isinstance(exc, dict) or isinstance(exc, str):
            return self.format_error_message(exc)
        try:
            error_message = str(exc)
            if exc.args:
                formatted_messages = []
                for arg in exc.args:
                    if isinstance(arg, dict):
                        for key, value in arg.items():
                            formatted_messages.append(f"{key}: {value}")
                    else:
                        formatted_messages.append(self.format_error_message(error_message))

                error_message = " ".join(formatted_messages)

            return error_message or EXCEPTIONS_MAP.get(type(exc), {}).get('message', _("A server error occurred"))
        except Exception as e:
            logger.error(f"Failed to format error message: {str(e)}")
            return EXCEPTIONS_MAP.get(type(exc), {}).get('message', _("A server error occurred"))


    def handle_exception(self, exc):
        error_status_code = EXCEPTIONS_MAP.get(type(exc), {}).get('status_code', HTTP_500_INTERNAL_SERVER_ERROR)
        error_message = self.get_error_message(exc)

        logger.error(f"Exception handled: {error_message}", exc_info=True)

        response = super().handle_exception(exc)

        custom_response_data = {
            'succeeded': False,
            'message': error_message,
            'code': error_status_code,
            'data': None,
        }

        response.data = custom_response_data

        return response

    @staticmethod
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
