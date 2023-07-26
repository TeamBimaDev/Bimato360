import csv
import django_filters
from django.db.models import Q
from pandas import read_csv
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from core.abstract.views import AbstractViewSet
from core.currency.models import BimaCoreCurrency
from core.currency.serializers import BimaCoreCurrencySerializer
from common.service.file_service import check_csv_file
from common.permissions.action_base_permission import ActionBasedPermission
from .service import import_data_from_csv_file


class CurrencyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    active = django_filters.ChoiceFilter(choices=[('True', 'True'), ('False', 'False'), ('all', 'all')],
                                         method='filter_active')

    class Meta:
        model = BimaCoreCurrency
        fields = ['active', 'name']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(symbol__icontains=value)
        )

    def filter_active(self, queryset, name, value):
        if value == 'all':
            return queryset
        else:
            return queryset.filter(active=(value == 'True'))


class BimaCoreCurrencyViewSet(AbstractViewSet):
    queryset = BimaCoreCurrency.objects.all()
    serializer_class = BimaCoreCurrencySerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    filterset_class = CurrencyFilter
    ordering_fields = AbstractViewSet.ordering_fields + \
                      ['symbol', 'name', 'active', 'currency_unit_label', 'currency_subunit_label']

    action_permissions = {
        'list': ['currency.can_read'],
        'export_data_to_csv': ['currency.can_read'],
        'create': ['currency.can_create'],
        'import_from_csv': ['currency.can_create'],
        'retrieve': ['currency.can_read'],
        'update': ['currency.can_update'],
        'partial_update': ['currency.can_update'],
        'destroy': ['currency.can_delete'],
    }

    def get_object(self):
        obj = BimaCoreCurrency.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    @action(detail=False, methods=["POST"], url_path="import_from_csv")
    def import_from_csv(self, request):
        csv_file = request.FILES.get("csv_file")

        try:
            file_check = check_csv_file(csv_file)
            if 'error' in file_check:
                return Response(file_check, status=status.HTTP_400_BAD_REQUEST)

            content_csv_file = read_csv(csv_file)
            error_rows, created_count = import_data_from_csv_file(content_csv_file)

            if error_rows:
                return Response({
                    'error': _('Some rows could not be processed'),
                    'error_rows': error_rows,
                    'success_rows_count': created_count,
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({'success': _('All rows processed successfully'),
                             'success_rows_count': created_count})

        except Exception:
            return Response({"error", _("an error occurred while treating the file")},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='export_data_to_csv')
    def export_data_to_csv(self, request):
        query = BimaCoreCurrency.objects.all()
        fields = query.model._meta
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename=currencies.csv'
        writer = csv.writer(response)
        fields_names = [field.name for field in fields.fields]
        writer.writerow(fields_names)
        for obj in query:
            writer.writerow(getattr(obj, field) for field in fields_names)
        return response
