from core.abstract.views import AbstractViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .filter import BimaTreasuryTransactionFilter
from .models import BimaTreasuryTransaction
from .serializers import BimaTreasuryTransactionSerializer, TransactionHistorySerializer
from .service import BimaTreasuryTransactionService
from ...common.permissions.action_base_permission import ActionBasedPermission


class BimaTreasuryTransactionViewSet(AbstractViewSet):
    queryset = BimaTreasuryTransaction.objects.all()
    serializer_class = BimaTreasuryTransactionSerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    ordering_fields = ['nature', 'direction', 'transaction_type', 'partner__name', 'amount', 'date']
    ordering = ['date']
    filterset_class = BimaTreasuryTransactionFilter
    action_permissions = {
        'list': ['transaction.can_read'],
        'create': ['transaction.can_create'],
        'retrieve': ['transaction.can_read'],
        'update': ['transaction.can_update'],
        'partial_update': ['transaction.can_update'],
        'destroy': ['transaction.can_delete'],
        'get_history_diff': ['transaction.can_view_history'],
    }

    def get_object(self):
        obj = BimaTreasuryTransaction.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    @action(detail=True, methods=['GET'], url_path='get_transaction_history')
    def get_transaction_history(self, request, pk=None):
        transaction = self.get_object()
        history = transaction.history.all()
        if not history.exists():
            return Response([], status=status.HTTP_200_OK)

        serialized_history = TransactionHistorySerializer(history, many=True)
        return Response(serialized_history.data)

    @action(detail=False, methods=['GET'], url_path='transaction_sums')
    def transaction_sums(self, request):
        filtered_qs = BimaTreasuryTransactionFilter(request.GET, queryset=BimaTreasuryTransaction.objects.all()).qs
        service = BimaTreasuryTransactionService(filtered_qs)
        result = service.calculate_sums()
        return Response(result)

    @action(detail=False, methods=['GET'], url_path='export_to_csv')
    def export_to_csv(self, request):
        filtered_qs = BimaTreasuryTransactionFilter(request.GET, queryset=BimaTreasuryTransaction.objects.all()).qs
        service = BimaTreasuryTransactionService(filtered_qs)
        file_path = service.export_to_csv("transactions_export.csv")
        return Response({"file_path": file_path})

    @action(detail=False, methods=['GET'], url_path='export_to_excel')
    def export_to_excel(self, request):
        filtered_qs = BimaTreasuryTransactionFilter(request.GET, queryset=BimaTreasuryTransaction.objects.all()).qs
        service = BimaTreasuryTransactionService(filtered_qs)
        file_path = service.export_to_excel("transactions_export.xlsx")
        return Response({"file_path": file_path})
