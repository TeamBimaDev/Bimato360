from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework import exceptions

class DefaultPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'
    ordering = '-created_at'

    def paginate_queryset(self, queryset, request, view=None):
        self.page_size = self.get_page_size(request)
        self.max_page_size = self.page_size

        filter_params = request.query_params.dict()
        if filter_params:
            filter_conditions = Q()
            for field, value in filter_params.items():
                field_condition = Q(**{field + '__icontains': value})
                filter_conditions &= field_condition
            queryset = queryset.filter(filter_conditions)

        paginated_queryset = super().paginate_queryset(queryset, request, view)

        count = queryset.count()
        total_pages = count // self.page_size
        if count % self.page_size > 0:
            total_pages += 1

        page_number = request.query_params.get(self.page_query_param, 1)
        self.page.number = page_number
        self.page.paginator.count = count
        self.page.paginator.num_pages = total_pages

        if self.page.number > total_pages:
            if total_pages > 0:
                self.page.number = total_pages
            else:
                raise exceptions.NotFound('Page not found.')

        return paginated_queryset
