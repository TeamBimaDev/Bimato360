from django.core.paginator import EmptyPage, InvalidPage
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DefaultPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 1000
    page_query_param = 'page'

    def paginate_queryset(self, queryset, request, view=None):
        try:
            return super().paginate_queryset(queryset, request, view)
        except (EmptyPage, NotFound):
            self.page = 1
            request.query_params._mutable = True
            request.query_params[self.page_query_param] = 1
            return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        if not data:
            return Response({
                'count': 0,
                'next': None,
                'previous': None,
                'results': []
            })

        return super().get_paginated_response(data)
