from core.abstract.views import AbstractViewSet
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from erp.partner.models import BimaErpPartner
from erp.partner.serializers import BimaErpPartnerSerializer
from core.document.models import BimaCoreDocument
from core.document.serializers import BimaCoreDocumentSerializer
from core.address.models import BimaCoreAddress
from core.address.serializers import BimaCoreAddressSerializer
from core.contact.models import BimaCoreContact
from core.contact.serializers import BimaCoreContactSerializer

from erp.partner.signals import post_create_partner


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
        post_create_partner.send(sender=self.__class__, instance=new_partner, address_data=address_data,
                                 contact_data=contact_data, document_data=document_data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        obj = BimaErpPartner.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    def list_documents(self, request, public_id=None):
        model = BimaCoreDocument
        serializer = BimaCoreDocumentSerializer
        return self.list_object(request, public_id=public_id, model=model, serializer=serializer)

    def list_contact(self, request, public_id=None):
        model = BimaCoreContact
        serializer = BimaCoreContactSerializer
        return self.list_object(request, public_id=public_id, model=model, serializer=serializer)

    def list_addresses(self, request, public_id=None):
        model = BimaCoreAddress
        serializer = BimaCoreAddressSerializer
        return self.list_object(request, public_id=public_id, model=model, serializer=serializer)



