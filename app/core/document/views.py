from common.enums.file_type import return_list_file_type_partner, return_list_file_purchase_document
from common.enums.file_type import return_list_file_type_user, return_list_file_type_company
from core.abstract.views import AbstractViewSet
from core.document.models import BimaCoreDocument
from core.document.serializers import BimaCoreDocumentGetSerializer
from core.document.serializers import BimaCoreDocumentSerializer
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class BimaCoreDocumentViewSet(AbstractViewSet):
    queryset = BimaCoreDocument.objects.all()
    serializer_class = BimaCoreDocumentSerializer
    permission_classes = []

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BimaCoreDocumentGetSerializer
        return BimaCoreDocumentSerializer

    def get_object(self):
        obj = BimaCoreDocument.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    def download_file(self, request, *args, **kwargs):
        document = BimaCoreDocument.objects.get_object_by_public_id(public_id=kwargs['public_id'])
        if document is not None:
            file_path = document.file_path.path
            file_name = document.document_name
            with open(file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type=document.file_content_type)
                response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                return response

        return Response(data=_("document not found"), status=status.HTTP_404_NOT_FOUND)

    def get_list_file_type_partner(self, request, *args, **kwargs):
        return Response(return_list_file_type_partner())

    @action(detail=False, methods=['get'], url_path='list_file_type_user')
    def user_documents_type(self, request, *args, **kwargs):
        return Response(return_list_file_type_user())

    @action(detail=False, methods=['get'], url_path='list_file_type_company')
    def company_documents_type(self, request, *args, **kwargs):
        return Response(return_list_file_type_company())

    @action(detail=False, methods=['get'], url_path='list_file_type_company')
    def company_documents_type(self, request, *args, **kwargs):
        return Response(return_list_file_type_company())

    @action(detail=False, methods=['GET'], url_path='list_file_type_purchase_document')
    def list_file_type_purchase_document(self, request, *args, **kwargs):
        return Response(return_list_file_purchase_document())
