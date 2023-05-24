from rest_framework.pagination import PageNumberPagination
from django.db.models import
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
        filter_param = request.query_params.get('filter')
        if filter_param:
            field_name, value = filter_param.split('=')
            filter_condition = Q(**{field_name: value})
            queryset = queryset.filter(filter_condition)
        paginated_queryset = super().paginate_queryset(queryset, request, view)
        self.page.paginator.count = queryset.count()
        self.page.paginator.num_pages = max(1, self.page.paginator.count // self.page_size)

        if self.page.number > self.page.paginator.num_pages:
            if self.page.paginator.num_pages > 0:
                self.page.number = self.page.paginator.num_pages
            else:
                raise exceptions.NotFound('Page not found.')
        return paginated_queryset
