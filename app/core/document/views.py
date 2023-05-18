from core.abstract.views import AbstractViewSet
from core.document.models import BimaCoreDocument

from core.document.serializers import BimaCoreDocumentSerializer
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


class BimaCoreDocumentViewSet(AbstractViewSet):
    queryset = BimaCoreDocument.objects.all()
    serializer_class = BimaCoreDocumentSerializer
    permission_classes = []

    def documentdownload(self, request, *args, **kwargs):
        document = get_object_or_404(BimaCoreDocument, pk=kwargs['pk'])
        response = HttpResponse(BimaCoreDocument.file_path, content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{document.file_path}"'
        return response
    def get_object(self):
        obj = BimaCoreDocument.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
