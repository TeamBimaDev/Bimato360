from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet
from core.entity_tag.models import (
    get_entity_tags_for_parent_entity,
    create_single_entity_tag,
    BimaCoreEntityTag,
)
from core.entity_tag.serializers import BimaCoreEntityTagSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .filter import BimaTreasuryTransactionFilter
from .models import BimaTreasuryTransaction
from .serializers import BimaTreasuryTransactionSerializer, TransactionHistorySerializer
from .service import BimaTreasuryTransactionService


class BimaTreasuryTransactionViewSet(AbstractViewSet):
    queryset = BimaTreasuryTransaction.objects.all()
    serializer_class = BimaTreasuryTransactionSerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    ordering_fields = [
        "nature",
        "direction",
        "transaction_type",
        "partner__name",
        "amount",
        "date",
    ]
    ordering = ["date"]
    filterset_class = BimaTreasuryTransactionFilter
    action_permissions = {
        "list": ["transaction.can_read"],
        "export_csv": ["transaction.can_read"],
        "export_excel": ["transaction.can_read"],
        "create": ["transaction.can_create"],
        "retrieve": ["transaction.can_read"],
        "update": ["transaction.can_update"],
        "partial_update": ["transaction.can_update"],
        "destroy": ["transaction.can_delete"],
        "get_transaction_history": ["transaction.can_view_history"],
    }

    def get_object(self):
        obj = BimaTreasuryTransaction.objects.get_object_by_public_id(self.kwargs["pk"])
        return obj

    @action(detail=True, methods=["GET"], url_path="get_transaction_history")
    def get_transaction_history(self, request, pk=None):
        transaction = self.get_object()
        history = transaction.history.all()
        if not history.exists():
            return Response([], status=status.HTTP_200_OK)

        serialized_history = TransactionHistorySerializer(history, many=True)
        return Response(serialized_history.data)

    @action(detail=False, methods=["GET"], url_path="transaction_sums")
    def transaction_sums(self, request):
        filtered_qs = BimaTreasuryTransactionFilter(
            request.GET, queryset=BimaTreasuryTransaction.objects.all()
        ).qs
        service = BimaTreasuryTransactionService(filtered_qs)
        result = service.calculate_sums()
        return Response(result)

    @action(detail=False, methods=["GET"], url_path="export_csv")
    def export_csv(self, request):
        filtered_qs = BimaTreasuryTransactionFilter(
            request.GET, queryset=BimaTreasuryTransaction.objects.all()
        ).qs
        service = BimaTreasuryTransactionService(filtered_qs)
        file_path = service.export_to_csv("transactions_export.csv")
        return Response({"file_path": file_path})

    @action(detail=False, methods=["GET"], url_path="export_excel")
    def export_excel(self, request):
        filtered_qs = BimaTreasuryTransactionFilter(
            request.GET, queryset=BimaTreasuryTransaction.objects.all()
        ).qs
        service = BimaTreasuryTransactionService(filtered_qs)
        file_path = service.export_to_excel("transactions_export.xlsx")
        return Response({"file_path": file_path})

    def list_tags(self, request, *args, **kwargs):
        transaction = BimaTreasuryTransaction.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        entity_tags = get_entity_tags_for_parent_entity(transaction).order_by("order")
        serialized_entity_tags = BimaCoreEntityTagSerializer(entity_tags, many=True)
        return Response(serialized_entity_tags.data)

    def create_tag(self, request, *args, **kwargs):
        transaction = BimaTreasuryTransaction.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        result = create_single_entity_tag(request.data, transaction)
        if isinstance(result, BimaCoreEntityTag):
            serialized_entity_tags = BimaCoreEntityTagSerializer(result)
            return Response(serialized_entity_tags.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                result,
                status=result.get("status", status.HTTP_500_INTERNAL_SERVER_ERROR),
            )

    def get_tag(self, request, *args, **kwargs):
        transaction = BimaTreasuryTransaction.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        entity_tags = get_object_or_404(
            BimaCoreEntityTag,
            public_id=self.kwargs["entity_tag_public_id"],
            parent_id=transaction.id,
        )
        if not entity_tags:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        serialized_entity_tags = BimaCoreEntityTagSerializer(entity_tags)
        return Response(serialized_entity_tags.data)

    @action(detail=False, methods=["GET"], url_path="available_transactions_years")
    def available_transactions_years(self, request, *args, **kwargs):
        years = BimaTreasuryTransaction.objects.dates("date", "year").values_list(
            "date__year", flat=True
        )
        return Response(years)
