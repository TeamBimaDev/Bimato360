from core.abstract.views import AbstractViewSet

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from erp.partner.models import BimaErpPartner
from erp.partner.serializers import BimaErpPartnerSerializer
from erp.partner.signals import post_create_partner

from core.address.serializers import BimaCoreAddressSerializer
from core.contact.serializers import BimaCoreContactSerializer
from core.document.serializers import BimaCoreDocumentSerializer

from core.address.models import BimaCoreAddress, get_addresses_for_parent, create_single_address
from core.contact.models import BimaCoreContact, create_single_contact, \
    get_contacts_for_parent_entity
from core.document.models import BimaCoreDocument, create_single_document,  \
    get_documents_for_parent_entity


class BimaErpPartnerViewSet(AbstractViewSet):
    queryset = BimaErpPartner.objects.all()
    serializer_class = BimaErpPartnerSerializer
    permission_classes = []

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
        post_create_partner.send(sender=self.__class__, instance=new_partner, address_data=address_data,
                                 contact_data=contact_data, document_data=document_data, tag_data=tag_data)

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
        address = get_object_or_404(BimaCoreAddress, public_id=self.kwargs['address_public_id'], parent_id=partner.id)
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
        contact = get_object_or_404(BimaCoreContact, public_id=self.kwargs['contact_public_id'], parent_id=partner.id)
        serialized_contact = BimaCoreContactSerializer(contact)
        return Response(serialized_contact.data)

    def list_documents(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(self.kwargs['public_id'])
        contacts = get_documents_for_parent_entity(partner)
        serialized_contact = BimaCoreDocumentSerializer(contacts, many=True)
        return Response(serialized_contact.data)

    def create_document(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(self.kwargs['public_id'])
        saved = create_single_document(request.data, partner)
        if not saved:
            return Response(saved.error, status=saved.status)
        return Response(saved)

    def get_document(self, request, *args, **kwargs):
        partner = BimaErpPartner.objects.get_object_by_public_id(self.kwargs['public_id'])
        document = get_object_or_404(BimaCoreDocument, public_id=self.kwargs['document_public_id'],
                                     parent_id=partner.id)
        serialized_document = BimaCoreContactSerializer(document)
        return Response(serialized_document.data)
