import csv
import django_filters
from core.abstract.views import AbstractViewSet
from django.db.models import Q

from django.http import HttpResponse, JsonResponse

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from .models import BimaErpPartner
from .serializers import BimaErpPartnerSerializer
from .signals import post_create_partner
from .utils import generate_xls_file
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
    ordering_fields = AbstractViewSet.ordering_fields + \
                      ['first_name', 'email', 'phone', 'partner_type']
    filterset_class = PartnerFilter

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
        saved = create_single_address(request.data, partner)
        if not saved:
            return Response(saved.error, status=saved.status)
        return Response(saved)

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
        saved = create_single_contact(request.data, partner)
        if not saved:
            return Response(saved.error, status=saved.status)
        return Response(saved)

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
        result = BimaCoreDocument.create_document_for_partner(partner, document_data)
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
        entity_tags = get_entity_tags_for_parent_entity(partner)
        serialized_entity_tags = BimaCoreEntityTagSerializer(entity_tags, many=True)
        return Response(serialized_entity_tags.data)

    def create_tag(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(self.kwargs['public_id'])
        result = create_single_entity_tag(request.data, partner)
        if isinstance(result, BimaCoreEntityTag):
            serializer = BimaCoreEntityTagSerializer(result)
            return Response({
                "id": result.public_id,
                "tag_name": result.tag.name
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

    def export_csv(self, request, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="partners.csv"'
        model_fields = BimaErpPartner._meta
        field_names_to_show = [fd.name for fd in model_fields.fields]
        writer = csv.writer(response)
        writer.writerow(field_names_to_show)
        if kwargs.get('public_id') is not None:
            data_to_export = [BimaErpPartner.objects.
                              get_object_by_public_id(kwargs.get('public_id'))]
        else:
            data_to_export = BimaErpPartner.objects.all()

        for partner in data_to_export:
            writer.writerow([getattr(partner, field) for field in field_names_to_show])

        return response

    def export_pdf(self, request, **kwargs):
        template_name = "partner/pdf.html"
        if kwargs.get('public_id') is not None:
            data_to_export = [BimaErpPartner.objects.
                              get_object_by_public_id(kwargs.get('public_id'))]
        else:
            data_to_export = BimaErpPartner.objects.all()

        return render_to_pdf(
            template_name,
            {
                "partners": data_to_export,
            },
            "partner.pdf"
        )

    def export_xls(self, request, **kwargs):
        model_fields = BimaErpPartner._meta

        if kwargs.get('public_id') is not None:
            data_to_export = [BimaErpPartner.objects.
                              get_object_by_public_id(kwargs.get('public_id'))]
        else:
            data_to_export = BimaErpPartner.objects.all()

        return generate_xls_file(data_to_export, model_fields)
