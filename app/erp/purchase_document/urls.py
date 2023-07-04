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
]
