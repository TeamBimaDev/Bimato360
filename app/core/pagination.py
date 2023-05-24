from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.response import Response

class DefaultPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'
    default_ordering = '-created_at'

    def paginate_queryset(self, queryset, request, view=None):
        self.page_size = self.get_page_size(request)
        self.max_page_size = self.page_size

        filter_params = request.query_params.dict()
        filtered_params = {k: v for k, v in filter_params.items() if not k.startswith('page')}

        filter_conditions = Q()
        for field, value in filtered_params.items():
            if field == 'ordering':
                ordering = value
            else:
                field_condition = Q(**{field + '__icontains': value})
                filter_conditions &= field_condition

        queryset = queryset.filter(filter_conditions)

        paginated_queryset = super().paginate_queryset(queryset, request, view)

        count = queryset.count()
        total_pages = count // self.page_size
        if count % self.page_size > 0:
            total_pages += 1

        page_number = int(request.query_params.get(self.page_query_param, 1))
        self.page.number = page_number
        self.page.paginator.count = count
        self.page.paginator.num_pages = total_pages

        if self.page.number > total_pages:
            if total_pages > 0:
                self.page.number = total_pages
            else:
                paginated_queryset = []

        return paginated_queryset

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })