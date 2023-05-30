from django.urls import path, include
from rest_framework.routers import DefaultRouter
from erp.partner.views import BimaErpPartnerViewSet

router = DefaultRouter()
router.register('', BimaErpPartnerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<str:public_id>/addresses/', BimaErpPartnerViewSet.as_view({'get': 'list_addresses'}),
         name='partner-addresses'),
    path('<str:public_id>/document/', BimaErpPartnerViewSet.as_view({'get': 'list_documents'}),
         name='document-partner'),
    path('<str:public_id>/contact/', BimaErpPartnerViewSet.as_view({'get': 'list_contact'}),
         name='document-partner'),
]
