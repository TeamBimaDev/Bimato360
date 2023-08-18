from core.abstract.views import AbstractViewSet
from core.pagination import DefaultPagination
from core.permissions import IsAdminOrReadOnly
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import BimaTreasuryTransaction
from .serializers import BimaTreasuryTransactionSerializer, TransactionHistorySerializer


class BimaTreasuryTransactionViewSet(AbstractViewSet):
    queryset = BimaTreasuryTransaction.objects.all()
    serializer_class = BimaTreasuryTransactionSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination

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
