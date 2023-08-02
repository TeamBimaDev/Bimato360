import logging
import os
from os.path import exists

import pytz
from common.converters.default_converters import str_to_bool
from common.enums.font_family import get_font_family_list
from common.permissions.action_base_permission import ActionBasedPermission
from common.service.file_service import get_available_template
from core.abstract.views import AbstractViewSet
from core.document.models import BimaCoreDocument, get_documents_for_parent_entity
from core.document.serializers import BimaCoreDocumentSerializer
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from app import settings
from .models import BimaCompany
from .serializers import BimaCompanySerializer
from .service import fetch_company_data, get_context

logger = logging.getLogger(__name__)


class BimaCompanyViewSet(AbstractViewSet):
    queryset = BimaCompany.objects.all()
    serializer_class = BimaCompanySerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        'list': ['company.can_read'],
        'create': ['company.can_create'],
        'get_available_templates_for_sale': ['company.can_create'],
        'generate_pdf_with_fake_data': ['company.can_create'],
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

    @action(detail=False, methods=['GET'], url_path='get_font_families')
    def get_font_families(self, request):
        return Response(get_font_family_list())

    @action(detail=False, methods=['GET'], url_path='get_available_templates_for_sale')
    def get_available_templates_for_sale(self, request):
        directory_path = os.path.join(settings.BASE_DIR, 'templates', 'sale_document', 'sale_templates')
        templates = get_available_template(directory_file=directory_path, file_extension='.html',
                                           file_name_prefix='sale_document_')
        return Response(templates)

    @action(detail=False, methods=['GET'], url_path='generate_pdf_with_fake_data')
    def generate_pdf_with_fake_data(self, request):
        request_data = self._load_data_from_request(request)
        default_sale_document_pdf_format = request_data.get('default_sale_document_pdf_format')
        if default_sale_document_pdf_format is None:
            return Response({'Error': _('Impossible de générer un appreçu du template')},
                            status=status.HTTP_400_BAD_REQUEST)

        template_directory_path = os.path.join(settings.BASE_DIR, 'templates', 'sale_document', 'sale_templates',
                                               default_sale_document_pdf_format)
        if not exists(template_directory_path):
            logger.error(
                f"Unable to find template file {default_sale_document_pdf_format} under {template_directory_path} ")
            return Response({'Error': _('Impossible de générer un appreçu du template')},
                            status=status.HTTP_400_BAD_REQUEST)

        context = get_context(request, request_data)

        template_name = f'sale_document/sale_templates/{default_sale_document_pdf_format}'
        template = get_template(template_name)
        html = template.render(context)
        return HttpResponse(html)

    def _load_data_from_request(self, request):
        default_sale_document_pdf_format = request.query_params.get('template_name')
        font_family = request.query_params.get('font_family', 'Arial')
        if font_family not in get_font_family_list():
            font_family = 'Arial'
        default_color = request.query_params.get('default_color', '#000000')
        show_template_header = str_to_bool(request.query_params.get('show_template_header', True))
        show_template_logo = str_to_bool(request.query_params.get('show_template_logo', True))
        show_template_footer = str_to_bool(request.query_params.get('show_template_footer', True))

        return {
            'default_sale_document_pdf_format': default_sale_document_pdf_format,
            'font_family': font_family,
            'default_color': default_color,
            'show_template_header': show_template_header,
            'show_template_footer': show_template_footer,
            'show_template_logo': show_template_logo,
        }
