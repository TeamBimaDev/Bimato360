from django.shortcuts import render

# Create your views here.
from .models import BimaPartners
from .serializers import BimaPartnersSerializer
from core.document.models import BimaCoreDocument
from core.document.serializers import BimaCoreDocumentSerializer
class BimaPartnersViewSet(AbstractViewSet):
    queryset = BimaPartners.objects.all()
    serializer_class = BimaPartnersSerializer
    permission_classes = []
    def list_documents(self, request, public_id=None):
        model = BimaCoreDocument
        serializer = BimaCoreDocumentSerializer
        return self.list_object(request, public_id=public_id, model=model, serializer=serializer)
