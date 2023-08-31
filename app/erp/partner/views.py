import django_filters
from common.converters.default_converters import str_to_bool
from common.enums.purchase_document_enum import PurchaseDocumentPaymentStatus, PurchaseDocumentStatus, \
    PurchaseDocumentTypes
from common.enums.sale_document_enum import (
    SaleDocumentPaymentStatus,
    SaleDocumentStatus,
    SaleDocumentTypes,
)
from common.permissions.action_base_permission import ActionBasedPermission
from common.service.file_service import check_csv_file
from common.utils.utils import render_to_pdf
from core.abstract.views import AbstractViewSet
from core.address.models import (
    BimaCoreAddress,
    get_addresses_for_parent,
    create_single_address,
)
from core.address.serializers import BimaCoreAddressSerializer
from core.contact.models import (
    BimaCoreContact,
    create_single_contact,
    get_contacts_for_parent_entity,
)
from core.contact.serializers import BimaCoreContactSerializer
from core.document.models import BimaCoreDocument, get_documents_for_parent_entity
from core.document.serializers import BimaCoreDocumentSerializer
from core.entity_tag.models import (
    BimaCoreEntityTag,
    create_single_entity_tag,
    get_entity_tags_for_parent_entity,
)
from core.entity_tag.serializers import BimaCoreEntityTagSerializer
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from erp.sale_document.serializers import BimaErpSaleDocumentUnpaidSerializer
from pandas import read_csv
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from treasury.bank_account.models import BimaTreasuryBankAccount
from treasury.bank_account.serializers import BimaTreasuryBankAccountSerializer
from treasury.bank_account.service import BimaTreasuryBankAccountService

from .models import BimaErpPartner
from .serializers import BimaErpPartnerSerializer
from .signals import post_create_partner
from .utils import generate_xls_file, import_partner_data_from_csv_file, export_to_csv


class PartnerFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")
    phone = django_filters.CharFilter(field_name="phone", lookup_expr="icontains")
    partner_type = django_filters.CharFilter(
        field_name="partner_type", lookup_expr="exact"
    )
    is_supplier = django_filters.BooleanFilter(method="filter_is_supplier")
    is_customer = django_filters.BooleanFilter(method="filter_is_customer")

    class Meta:
        model = BimaErpPartner
        fields = ["phone", "partner_type", "search"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value)
            | Q(last_name__icontains=value)
            | Q(company_name__icontains=value)
        )

    def filter_is_supplier(self, queryset, name, value):
        if value is not None:
            return queryset.filter(is_supplier=str_to_bool(value))

    def filter_is_customer(self, queryset, name, value):
        if value is not None:
            return queryset.filter(is_customer=str_to_bool(value))


class BimaErpPartnerViewSet(AbstractViewSet):
    queryset = BimaErpPartner.objects.all()
    serializer_class = BimaErpPartnerSerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    ordering_fields = ["first_name", "email", "phone", "partner_type"]
    ordering = ["created"]
    filterset_class = PartnerFilter
    action_permissions = {
        "list": ["partner.can_read"],
        "export_csv": ["partner.can_read"],
        "export_xls": ["partner.can_read"],
        "export_pdf": ["partner.can_read"],
        "create": ["partner.can_create"],
        "generate_partner_from_csv": ["partner.can_create"],
        "retrieve": ["partner.can_read"],
        "update": ["partner.can_update"],
        "partial_update": ["partner.can_update"],
        "destroy": ["partner.can_delete"],
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        new_partner = get_object_or_404(
            BimaErpPartner, public_id=serializer.data["public_id"]
        )

        address_data = request.data.get("address_data", [])
        contact_data = request.data.get("contact_data", [])
        document_data = request.data.get("document_data", [])
        tag_data = request.data.get("tag_data", [])
        post_create_partner.send(
            sender=self.__class__,
            instance=new_partner,
            address_data=address_data,
            contact_data=contact_data,
            document_data=document_data,
            tag_data=tag_data,
        )

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_object(self):
        obj = BimaErpPartner.objects.get_object_by_public_id(self.kwargs["pk"])
        return obj

    def list_addresses(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        addresses = get_addresses_for_parent(partner)
        serialized_addresses = BimaCoreAddressSerializer(addresses, many=True)
        return Response(serialized_addresses.data)

    def create_address(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        response = create_single_address(request.data, partner)
        if "error" in response:
            return Response({"detail": response["error"]}, status=response["status"])
        return Response(response["data"], status=response["status"])

    def get_address(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        address = get_object_or_404(
            BimaCoreAddress,
            public_id=self.kwargs["address_public_id"],
            parent_id=partner.id,
        )
        serialized_address = BimaCoreAddressSerializer(address)
        return Response(serialized_address.data)

    def list_contacts(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        contacts = get_contacts_for_parent_entity(partner)
        serialized_contact = BimaCoreContactSerializer(contacts, many=True)
        return Response(serialized_contact.data)

    def create_contact(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        response = create_single_contact(request.data, partner)
        if "error" in response:
            return Response({"detail": response["error"]}, status=response["status"])
        return Response(response["data"], status=response["status"])

    def get_contact(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        contact = get_object_or_404(
            BimaCoreContact,
            public_id=self.kwargs["contact_public_id"],
            parent_id=partner.id,
        )
        serialized_contact = BimaCoreContactSerializer(contact)
        return Response(serialized_contact.data)

    def list_documents(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        contacts = get_documents_for_parent_entity(partner)
        serialized_contact = BimaCoreDocumentSerializer(contacts, many=True)
        return Response(serialized_contact.data)

    def create_document(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        document_data = request.data
        document_data["file_path"] = request.FILES["file_path"]
        result = BimaCoreDocument.create_document_for_parent(partner, document_data)
        if isinstance(result, BimaCoreDocument):
            return Response(
                {
                    "id": result.public_id,
                    "document_name": result.document_name,
                    "description": result.description,
                    "date_file": result.date_file,
                    "file_type": result.file_type,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                result,
                status=result.get("status", status.HTTP_500_INTERNAL_SERVER_ERROR),
            )

    def get_document(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        document = get_object_or_404(
            BimaCoreDocument,
            public_id=self.kwargs["document_public_id"],
            parent_id=partner.id,
        )
        serialized_document = BimaCoreDocumentSerializer(document)
        return Response(serialized_document.data)

    def list_tags(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        entity_tags = get_entity_tags_for_parent_entity(partner).order_by("order")
        serialized_entity_tags = BimaCoreEntityTagSerializer(entity_tags, many=True)
        return Response(serialized_entity_tags.data)

    def create_tag(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        result = create_single_entity_tag(request.data, partner)
        if isinstance(result, BimaCoreEntityTag):
            serializer = BimaCoreEntityTagSerializer(result)
            return Response(
                {
                    "id": result.public_id,
                    "tag_name": result.tag.name,
                    "order": result.order,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                result,
                status=result.get("status", status.HTTP_500_INTERNAL_SERVER_ERROR),
            )

    def get_tag(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        entity_tags = get_object_or_404(
            BimaCoreEntityTag,
            public_id=self.kwargs["entity_tag_public_id"],
            parent_id=partner.id,
        )
        serialized_entity_tags = BimaCoreEntityTagSerializer(entity_tags)
        return JsonResponse(serialized_entity_tags.data)

    def list_bank_account(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        bank_accounts = (
            BimaTreasuryBankAccountService.get_bank_accounts_for_parent_entity(partner)
        )
        serialized_contact = BimaTreasuryBankAccountSerializer(bank_accounts, many=True)
        return Response(serialized_contact.data)

    def create_bank_account(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        bank_account_data = request.data
        result = BimaTreasuryBankAccountService.create_bank_account(
            partner, bank_account_data
        )
        if isinstance(result, BimaTreasuryBankAccount):
            serialized_document = BimaTreasuryBankAccountSerializer(result)
            return Response(serialized_document.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                result,
                status=result.get("status", status.HTTP_500_INTERNAL_SERVER_ERROR),
            )

    def get_bank_account(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        bank_account = (
            BimaTreasuryBankAccountService.get_bank_account_by_public_id_and_parent(
                public_id=self.kwargs["bank_account_public_id"], parent_id=partner.id
            )
        )
        if not bank_account:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        serialized_account = BimaTreasuryBankAccountSerializer(bank_account)
        return Response(serialized_account.data)

    @action(detail=False, methods=["GET"], url_path="export_csv")
    def export_csv(self, request):
        data_to_export = self.get_queryset()
        filtered_data = PartnerFilter(request.GET, queryset=data_to_export)
        model_fields = BimaErpPartner._meta
        return export_to_csv(filtered_data.qs, model_fields)

    @action(detail=True, methods=["GET"], url_path="export_csv")
    def detail_export_csv(self, request, pk=None):
        data_to_export = [self.get_object()]
        model_fields = BimaErpPartner._meta
        return export_to_csv(data_to_export, model_fields)

    @action(detail=False, methods=["GET"], url_path="export_pdf")
    def export_pdf(self, request):
        template_name = "partner/pdf.html"
        data_to_export = self.get_queryset()
        filtered_data = PartnerFilter(request.GET, queryset=data_to_export)
        return render_to_pdf(
            template_name,
            {
                "partners": filtered_data.qs,
                "request": request,
            },
            "partner.pdf",
        )

    @action(detail=True, methods=["GET"], url_path="export_pdf")
    def detail_export_pdf(self, request, pk=None):
        template_name = "partner/pdf.html"
        data_to_export = [self.get_object()]
        return render_to_pdf(
            template_name,
            {
                "partners": data_to_export,
                "request": request,
            },
            "partner.pdf",
        )

    @action(detail=False, methods=["GET"], url_path="export_xls")
    def export_xls(self, request):
        data_to_export = self.get_queryset()
        filtered_data = PartnerFilter(request.GET, queryset=data_to_export)
        return generate_xls_file(filtered_data.qs)

    @action(detail=True, methods=["GET"], url_path="export_xls")
    def detail_export_xls(self, request, pk=None):
        data_to_export = [self.get_object()]
        return generate_xls_file(data_to_export)

    @action(detail=False, methods=["POST"], url_path="import_from_csv")
    def import_from_csv(self, request):
        csv_file = request.FILES.get("csv_file")

        try:
            file_check = check_csv_file(csv_file)
            if "error" in file_check:
                return Response(file_check, status=status.HTTP_400_BAD_REQUEST)

            csv_content_file = read_csv(csv_file)

            error_rows, created_count = import_partner_data_from_csv_file(
                csv_content_file
            )
            if error_rows:
                return Response(
                    {
                        "error": _("Some rows could not be processed"),
                        "error_rows": error_rows,
                        "success_rows_count": created_count,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                {
                    "success": _("All rows processed successfully"),
                    "success_rows_count": created_count,
                }
            )

        except Exception:
            return Response(
                {"error", _("an error occurred while treating the file")},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["GET"], url_path="get_unpaid_invoice")
    def get_unpaid_invoice(self, request, pk=None):
        partner = self.get_object()
        unpaid_invoice = partner.bimaerpsaledocument_set.exclude(
            payment_status=SaleDocumentPaymentStatus.PAID.name
        ).filter(
            status=SaleDocumentStatus.CONFIRMED.name,
            type=SaleDocumentTypes.INVOICE.name,
        )

        serialized_data = BimaErpSaleDocumentUnpaidSerializer(unpaid_invoice, many=True)
        return Response(serialized_data.data)

    @action(detail=True, methods=["GET"], url_path="get_unpaid_invoice")
    def get_unpaid_invoice_supplier(self, request, pk=None):
        partner = self.get_object()
        unpaid_invoice = partner.bimaerppurchasedocument_set.exclude(
            payment_status=PurchaseDocumentPaymentStatus.PAID.name
        ).filter(
            status=PurchaseDocumentStatus.CONFIRMED.name,
            type=PurchaseDocumentTypes.INVOICE.name,
        )

        serialized_data = BimaErpSaleDocumentUnpaidSerializer(unpaid_invoice, many=True)
        return Response(serialized_data.data)
