from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaHrContractViewSet

router = DefaultRouter()

router.register('', BimaHrContractViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<str:public_id>/documents/',
         BimaHrContractViewSet.as_view({'get': 'list_documents', 'post': 'create_document'}),
         name='contract-documents'),
    path('<str:public_id>/documents/<str:document_public_id>/',
         BimaHrContractViewSet.as_view({'get': 'get_document'}),
         name='contract-document'),
]
