from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import filters

from .base_filter import BaseFilter
from .pagination import DefaultPagination

from rest_framework.exceptions import NotFound, APIException, ValidationError, AuthenticationFailed, PermissionDenied
from django.core.exceptions import ObjectDoesNotExist


class AbstractViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = BaseFilter
    ordering_fields = ['updated', 'created']
    ordering = ['-updated']
    pagination_class = DefaultPagination

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            exc = APIException('There was a validation error.')
        elif isinstance(exc, AuthenticationFailed):
            exc = APIException('Authentication failed.')
        elif isinstance(exc, PermissionDenied):
            exc = APIException('Permission was denied.')
        elif isinstance(exc, ObjectDoesNotExist) or isinstance(exc, Http404):
            exc = NotFound('The partner or the item does not exist.')
        else:
            exc = APIException('A server error occurred.')
        response = super().handle_exception(exc)

        # Customize the response format
        custom_response_data = {
            'succeeded': False,
            'message': response.data['detail'] if 'detail' in response.data else 'A server error occurred.',
            'code': response.status_code,
            'data': None,
        }

        response.data = custom_response_data

        return response
