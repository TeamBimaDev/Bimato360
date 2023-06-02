from django.urls import path, include
from rest_framework.routers import DefaultRouter
from erp.partner.views import BimaErpPartnerViewSet

router = DefaultRouter()
router.register('', BimaErpPartnerViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('<str:public_id>/addresses/',
         BimaErpPartnerViewSet.as_view({'get': 'list_addresses', 'post': 'create_address'}),
         name='partner-addresses'),
    path('<str:public_id>/addresses/<str:address_public_id>/',
         BimaErpPartnerViewSet.as_view({'get': 'get_address'}),
         name='partner-get-address'),


    path('<str:public_id>/contacts/',
         BimaErpPartnerViewSet.as_view({'get': 'list_contacts', 'post': 'create_contact'}),
         name='partner-contacts'),
    path('<str:public_id>/contacts/<str:contact_public_id>/',
         BimaErpPartnerViewSet.as_view({'get': 'get_contact'}),
         name='partner-contact'),

    path('<str:public_id>/documents/',
         BimaErpPartnerViewSet.as_view({'get': 'list_documents', 'post': 'create_document'}),
         name='partner-documents'),
    path('<str:public_id>/documents/<str:document_public_id>/',
         BimaErpPartnerViewSet.as_view({'get': 'get_document'}),
         name='partner-document'),

    path('export_csv',
         BimaErpPartnerViewSet.as_view({'get': 'export_data_csv'}),
         name='partner-export_csv'),
    path('<str:public_id>/export_csv',
         BimaErpPartnerViewSet.as_view({'get': 'export_data_csv'}),
         name='partner-export_csv'),

    path('export_pdf',
         BimaErpPartnerViewSet.as_view({'get': 'generate_pdf'}),
         name='partner-export_pdf'),
    path('<str:public_id>/export_pdf',
         BimaErpPartnerViewSet.as_view({'get': 'generate_pdf'}),
         name='partner-export_pdf'),
]
