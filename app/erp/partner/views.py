import django_filters
from core.abstract.views import AbstractViewSet
from django.db.models import Q
from pandas import read_csv
from rest_framework.decorators import action

from django.http import JsonResponse

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from .models import BimaErpPartner
from .serializers import BimaErpPartnerSerializer
from .signals import post_create_partner
from .utils import generate_xls_file, import_partner_data_from_csv_file, export_to_csv

from common.utils.utils import render_to_pdf
from core.address.serializers import BimaCoreAddressSerializer
from core.address.models import BimaCoreAddress, get_addresses_for_parent, create_single_address

from core.contact.serializers import BimaCoreContactSerializer
from core.contact.models import BimaCoreContact, create_single_contact, \
    get_contacts_for_parent_entity

from core.document.serializers import BimaCoreDocumentSerializer
from core.document.models import BimaCoreDocument, create_single_document, \
    get_documents_for_parent_entity

from core.entity_tag.serializers import BimaCoreEntityTagSerializer
from core.entity_tag.models import BimaCoreEntityTag, create_single_entity_tag, \
    get_entity_tags_for_parent_entity
from common.permissions.action_base_permission import ActionBasedPermission

from common.service.file_service import check_csv_file
from django.utils.translation import gettext_lazy as _


class PartnerFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    phone = django_filters.CharFilter(field_name='phone', lookup_expr='icontains')
    partner_type = django_filters.CharFilter(field_name='partner_type', lookup_expr='exact')

    class Meta:
        model = BimaErpPartner
        fields = ['phone', 'partner_type', 'search']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(company_name__icontains=value)
        )


class BimaErpPartnerViewSet(AbstractViewSet):
    queryset = BimaErpPartner.objects.all()
    serializer_class = BimaErpPartnerSerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    ordering_fields = ['first_name', 'email', 'phone', 'partner_type']
    ordering = ['created']
    filterset_class = PartnerFilter
    action_permissions = {
        'list': ['partner.can_read'],
        'export_csv': ['partner.can_read'],
        'export_xls': ['partner.can_read'],
        'export_pdf': ['partner.can_read'],
        'create': ['partner.can_create'],
        'generate_partner_from_csv': ['partner.can_create'],
        'retrieve': ['partner.can_read'],
        'update': ['partner.can_update'],
        'partial_update': ['partner.can_update'],
        'destroy': ['partner.can_delete'],
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        new_partner = get_object_or_404(BimaErpPartner, public_id=serializer.data['public_id'])

        address_data = request.data.get('address_data', [])
        contact_data = request.data.get('contact_data', [])
        document_data = request.data.get('document_data', [])
        tag_data = request.data.get('tag_data', [])
        post_create_partner.send(sender=self.__class__, instance=new_partner,
                                 address_data=address_data,
                                 contact_data=contact_data,
                                 document_data=document_data,
                                 tag_data=tag_data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        obj = BimaErpPartner.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    def list_addresses(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(self.kwargs['public_id'])
        addresses = get_addresses_for_parent(partner)
        serialized_addresses = BimaCoreAddressSerializer(addresses, many=True)
        return Response(serialized_addresses.data)

    def create_address(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(self.kwargs['public_id'])
        response = create_single_address(request.data, partner)
        if "error" in response:
            return Response({"detail": response["error"]}, status=response["status"])
        return Response(response["data"], status=response["status"])

    def get_address(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(self.kwargs['public_id'])
        address = get_object_or_404(BimaCoreAddress,
                                    public_id=self.kwargs['address_public_id'],
                                    parent_id=partner.id)
        serialized_address = BimaCoreAddressSerializer(address)
        return Response(serialized_address.data)

    def list_contacts(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(self.kwargs['public_id'])
        contacts = get_contacts_for_parent_entity(partner)
        serialized_contact = BimaCoreContactSerializer(contacts, many=True)
        return Response(serialized_contact.data)

    def create_contact(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(self.kwargs['public_id'])
        response = create_single_contact(request.data, partner)
        if "error" in response:
            return Response({"detail": response["error"]}, status=response["status"])
        return Response(response["data"], status=response["status"])

    def get_contact(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(self.kwargs['public_id'])
        contact = get_object_or_404(BimaCoreContact,
                                    public_id=self.kwargs['contact_public_id'],
                                    parent_id=partner.id)
        serialized_contact = BimaCoreContactSerializer(contact)
        return Response(serialized_contact.data)

    def list_documents(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(self.kwargs['public_id'])
        contacts = get_documents_for_parent_entity(partner)
        serialized_contact = BimaCoreDocumentSerializer(contacts, many=True)
        return Response(serialized_contact.data)

    def create_document(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(self.kwargs['public_id'])
        document_data = request.data
        document_data['file_path'] = request.FILES['file_path']
        result = BimaCoreDocument.create_document_for_parent(partner, document_data)
        if isinstance(result, BimaCoreDocument):
            return Response({
                "id": result.public_id,
                "document_name": result.document_name,
                "description": result.description,
                "date_file": result.date_file,
                "file_type": result.file_type

            }, status=status.HTTP_201_CREATED)
        else:
            return Response(result, status=result.get("status", status.HTTP_500_INTERNAL_SERVER_ERROR))

    def get_document(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(self.kwargs['public_id'])
        document = get_object_or_404(BimaCoreDocument,
                                     public_id=self.kwargs['document_public_id'],
                                     parent_id=partner.id)
        serialized_document = BimaCoreContactSerializer(document)
        return Response(serialized_document.data)

    def list_tags(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(self.kwargs['public_id'])
        entity_tags = get_entity_tags_for_parent_entity(partner).order_by('order')
        serialized_entity_tags = BimaCoreEntityTagSerializer(entity_tags, many=True)
        return Response(serialized_entity_tags.data)

    def create_tag(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(self.kwargs['public_id'])
        result = create_single_entity_tag(request.data, partner)
        if isinstance(result, BimaCoreEntityTag):
            serializer = BimaCoreEntityTagSerializer(result)
            return Response({
                "id": result.public_id,
                "tag_name": result.tag.name,
                "order": result.order,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(result, status=result.get("status", status.HTTP_500_INTERNAL_SERVER_ERROR))

    def get_tag(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(self.kwargs['public_id'])
        entity_tags = get_object_or_404(BimaCoreEntityTag,
                                        public_id=self.kwargs['entity_tag_public_id'],
                                        parent_id=partner.id)
        serialized_entity_tags = BimaCoreEntityTagSerializer(entity_tags)
        return JsonResponse(serialized_entity_tags.data)

    def get_data_to_export(self, kwargs):
        if kwargs.get('public_id') is not None:
            data_to_export = [BimaErpPartner.objects.
                              get_object_by_public_id(kwargs.get('public_id'))]
        else:
            data_to_export = BimaErpPartner.objects.all()
        return data_to_export

    def export_csv(self, request, **kwargs):
        data_to_export = self.get_data_to_export(kwargs)
        model_fields = BimaErpPartner._meta
        return export_to_csv(data_to_export, model_fields)

    def export_pdf(self, request, **kwargs):
        template_name = "partner/pdf.html"
        data_to_export = self.get_data_to_export(kwargs)

        return render_to_pdf(
            template_name,
            {
                "partners": data_to_export,
                "request": request,
            },
            "partner.pdf"
        )

    def export_xls(self, request, **kwargs):
        data_to_export = self.get_data_to_export(kwargs)
        return generate_xls_file(data_to_export)

    @action(detail=False, methods=['POST'], url_path='import_from_csv')
    def import_from_csv(self, request):
        csv_file = request.FILES.get['csv_file']

        try:
            file_check = check_csv_file(csv_file)
            if 'error' in file_check:
                return Response(file_check, status=status.HTTP_400_BAD_REQUEST)

            csv_content_file = read_csv(csv_file)

            error_rows, created_count = import_partner_data_from_csv_file(csv_content_file)
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
