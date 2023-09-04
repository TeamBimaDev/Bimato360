import uuid
from io import BytesIO

from common.enums.transaction_enum import TransactionDirection
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet
from core.entity_tag.models import (
    get_entity_tags_for_parent_entity,
    create_single_entity_tag,
    BimaCoreEntityTag,
)
from core.entity_tag.serializers import BimaCoreEntityTagSerializer
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from openpyxl.reader.excel import load_workbook
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .filter import BimaTreasuryTransactionFilter
from .models import BimaTreasuryTransaction, TransactionSaleDocumentPayment, TransactionPurchaseDocumentPayment
from .serializers import BimaTreasuryTransactionSerializer, TransactionHistorySerializer, \
    TransactionSaleDocumentPaymentSerializer, TransactionPurchaseDocumentPaymentSerializer
from .service import BimaTreasuryTransactionService
from .service_payment_invoice import handle_invoice_payment, get_invoice_payment_customer_codes


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

    def perform_create(self, serializer):
        sale_document_public_ids = self.request.data.pop('sale_documents_ids')
        instance = serializer.save()
        handle_invoice_payment(instance, sale_document_public_ids)

    def perform_update(self, serializer):
        sale_document_public_ids = self.request.data.pop('sale_documents_ids')
        instance = serializer.save()
        handle_invoice_payment(instance, sale_document_public_ids)

    @action(detail=False, methods=['get'])
    def get_unique_number(self, request, **kwargs):
        try:
            unique_number = BimaTreasuryTransactionService.generate_unique_number()
            return Response({"unique_number": unique_number})
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"], url_path="get_transaction_history")
    def get_transaction_history(self, request, pk=None):
        transaction = self.get_object()
        history = transaction.history.all()
        if not history.exists():
            return Response([], status=status.HTTP_200_OK)

        serialized_history = TransactionHistorySerializer(history, many=True).data
        grouped_history = BimaTreasuryTransactionService.group_by_date(
            serialized_history
        )
        response_data = [
            {"date": key, "changes": value} for key, value in grouped_history.items()
        ]
        return Response(response_data)

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
        df = service.export_to_csv()

        buffer = BytesIO()
        df.to_csv(buffer, index=False)

        response = HttpResponse(buffer.getvalue(), content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=transactions_export.csv"

        return response

    @action(detail=False, methods=["GET"], url_path="export_xls")
    def export_xls(self, request):
        filtered_qs = BimaTreasuryTransactionFilter(
            request.GET, queryset=BimaTreasuryTransaction.objects.all()
        ).qs
        service = BimaTreasuryTransactionService(filtered_qs)
        df = service.export_to_excel()

        buffer = BytesIO()
        df.to_excel(buffer, index=False, engine="openpyxl")
        buffer.seek(0)

        wb = load_workbook(buffer)
        ws = wb.active
        service.style_worksheet(ws)
        service.append_totals(ws)

        buffer.seek(0)
        wb.save(buffer)

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response[
            "Content-Disposition"
        ] = "attachment; filename=transactions_export.xlsx"

        return response

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

    @action(detail=True, methods=['GET'], url_path='transaction_sale_document_payments')
    def transaction_sale_document_payments(self, request, pk=None):
        transaction = self.get_object()
        sale_document_payments = TransactionSaleDocumentPayment.objects.filter(transaction=transaction)
        serializer = TransactionSaleDocumentPaymentSerializer(sale_document_payments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], url_path='transaction_purchase_document_payments')
    def transaction_purchase_document_payments(self, request, pk=None):
        transaction = self.get_object()
        purchase_document_payments = TransactionPurchaseDocumentPayment.objects.filter(transaction=transaction)
        serializer = TransactionPurchaseDocumentPaymentSerializer(purchase_document_payments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path='get_transactions_with_remaining_amount')
    def transaction_purchase_document_payments(self, request):
        partner_public_id = request.query_params.get('partner_public_id')
        transactions = BimaTreasuryTransaction.objects.filter(
            remaining_amount__gt=0,
            direction=TransactionDirection.INCOME.name,
            transaction_type__code__in=get_invoice_payment_customer_codes(),
            partner__public_id=partner_public_id
        )
        serializer = BimaTreasuryTransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path='transaction_by_sale_document')
    def transaction_by_sale_document(self, request, pk=None):
        sale_document_public_id = request.query_params.get('sale_document_public_id')
        if not sale_document_public_id or not uuid.UUID(sale_document_public_id, version=4):
            return Response({"Error": _("Please provide a valid UUID")}, status=status.HTTP_400_BAD_REQUEST)

        sale_document_payments = TransactionSaleDocumentPayment.objects.filter(
            sale_document__public_id=sale_document_public_id)
        serializer = TransactionSaleDocumentPaymentSerializer(sale_document_payments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path='transaction_by_purchase_document')
    def transaction_by_purchase_document(self, request, pk=None):
        purchase_document_public_id = request.query_params.get('purchase_document_public_id')
        if not purchase_document_public_id or not uuid.UUID(purchase_document_public_id, version=4):
            return Response({"Error": _("Please provide a valid UUID")}, status=status.HTTP_400_BAD_REQUEST)

        purchase_document_payments = TransactionPurchaseDocumentPayment.objects.filter(
            purchase_document__public_id=purchase_document_public_id)
        serializer = TransactionPurchaseDocumentPaymentSerializer(purchase_document_payments, many=True)
        return Response(serializer.data)
