from core.abstract.views import AbstractViewSet
from core.currency.models import BimaCoreCurrency
from core.currency.serializers import BimaCoreCurrencySerializer
from common.permissions.action_base_permission import ActionBasedPermission
from requests import Response
from rest_framework import status
from rest_framework.decorators import action
from django.utils.translation import gettext_lazy as _

from .service import import_data_from_csv_file
from pandas import read_csv
from common.service.file_service import check_csv_file


class BimaCoreCurrencyViewSet(AbstractViewSet):
    queryset = BimaCoreCurrency.objects.all()
    serializer_class = BimaCoreCurrencySerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    ordering_fields = AbstractViewSet.ordering_fields + \
                      ['symbol', 'name', 'active', 'currency_unit_label', 'currency_subunit_label']

    action_permissions = {
        'list': ['currency.can_read'],
        'create': ['currency.can_create'],
        'retrieve': ['currency.can_read'],
        'update': ['currency.can_update'],
        'partial_update': ['currency.can_update'],
        'destroy': ['currency.can_delete'],
    }

    def get_object(self):
        obj = BimaCoreCurrency.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    @action(detail=False, methods=["post"], url_path="import_form_csv")
    def import_from_csv(self, request, **kwargs):
        csv_file = request.FILE.get("file")

        try:
            file_check = check_csv_file(csv_file)
            if 'error' in file_check:
                return Response(file_check, status=status.HTTP_400_BAD_REQUEST)

            content_csv_file = read_csv(csv_file)
            error_rows, created_count = import_data_from_csv_file(content_csv_file)

            if error_rows:
                return Response({
                    'error': _('Some rows could not be processed'),
                    _('error_rows'): error_rows,
                    _('success_rows_count'): created_count,
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({'success': _('All rows processed successfully'),
                             _('success_rows_count'): created_count})

        except Exception:
            return Response({"error", _("an error occurred while treating the file")},
                            status=status.HTTP_400_BAD_REQUEST)

