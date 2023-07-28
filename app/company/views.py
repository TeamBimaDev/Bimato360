import pytz
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from common.permissions.action_base_permission import ActionBasedPermission

from core.document.serializers import BimaCoreDocumentSerializer
from core.abstract.views import AbstractViewSet
from core.document.models import BimaCoreDocument, create_single_document, \
    get_documents_for_parent_entity

from .models import BimaCompany
from .serializers import BimaCompanySerializer
from .service import fetch_company_data


class BimaCompanyViewSet(AbstractViewSet):
    queryset = BimaCompany.objects.all()
    serializer_class = BimaCompanySerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        'list': ['company.can_read'],
        'create': ['company.can_create'],
        'retrieve': ['company.can_read'],
        'update': ['company.can_update'],
        'partial_update': ['company.can_update'],
        'destroy': ['company.can_delete'],
        'documents': ['company.can_add_document'],
    }

    def list_documents(self, request, *args, **kwargs):
        company = BimaCompany.objects.get_object_by_public_id(self.kwargs['public_id'])
        documents = get_documents_for_parent_entity(company)
        serialized_contact = BimaCoreDocumentSerializer(documents, many=True)
        return Response(serialized_contact.data)

    def create_document(self, request, *args, **kwargs):
        company = BimaCompany.objects.get_object_by_public_id(self.kwargs['public_id'])
        document_data = request.data
        document_data['file_path'] = request.FILES['file_path']
        document_data['is_favorite'] = request.data.get('is_favorite', False)
        result = BimaCoreDocument.create_document_for_parent(company, document_data)
        if isinstance(result, BimaCoreDocument):
            return Response({
                "id": result.public_id,
                "document_name": result.document_name,
                "description": result.description,
                "date_file": result.date_file,
                "file_type": result.file_type,
                "is_favorite": result.is_favorite

            }, status=status.HTTP_201_CREATED)
        else:
            return Response(result, status=result.get("status", status.HTTP_500_INTERNAL_SERVER_ERROR))

    def get_document(self, request, *args, **kwargs):
        company = BimaCompany.objects.get_object_by_public_id(self.kwargs['public_id'])
        document = get_object_or_404(BimaCoreDocument,
                                     public_id=self.kwargs['document_public_id'],
                                     parent_id=company.id)
        serialized_document = BimaCoreDocumentSerializer(document)
        return Response(serialized_document.data)

    def get_object(self):
        obj = BimaCompany.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    @action(detail=True, methods=['get'], url_path='get_company_data_for_pdf')
    def get_company_data_for_pdf(self, request, *args, **kwargs):
        company = self.get_object()
        response_data = fetch_company_data(company)
        return Response(response_data)

    @action(detail=False, methods=['GET'], url_path='get_timezones')
    def get_timezones(self, request):
        timezones = [{'id': tz, 'name': tz} for tz in pytz.all_timezones]
        return Response(timezones)
