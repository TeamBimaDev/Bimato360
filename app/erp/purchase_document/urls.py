<<<<<<< HEAD
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaErpPurchaseDocumentViewSet

router = DefaultRouter()
router.register('', BimaErpPurchaseDocumentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create_new_document_from_parent/',
         BimaErpPurchaseDocumentViewSet.as_view({'post': 'create_new_document_from_parent'}),
         name='create_new_document_from_parent'),

    path('<str:public_id>/documents/',
         BimaErpPurchaseDocumentViewSet.as_view({'get': 'list_documents', 'post': 'create_document'}),
         name='company-documents'),
    path('<str:public_id>/documents/<str:document_public_id>/',
         BimaErpPurchaseDocumentViewSet.as_view({'get': 'get_document'}),
         name='company-document'),
]
=======
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaErpPurchaseDocumentViewSet

router = DefaultRouter()
router.register('', BimaErpPurchaseDocumentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create_new_document_from_parent/',
         BimaErpPurchaseDocumentViewSet.as_view({'post': 'create_new_document_from_parent'}),
         name='create_new_document_from_parent'),

    path('<str:public_id>/documents/',
         BimaErpPurchaseDocumentViewSet.as_view({'get': 'list_documents', 'post': 'create_document'}),
         name='company-documents'),
    path('<str:public_id>/documents/<str:document_public_id>/',
         BimaErpPurchaseDocumentViewSet.as_view({'get': 'get_document'}),
         name='company-document'),
]
>>>>>>> origin/ma-branch
