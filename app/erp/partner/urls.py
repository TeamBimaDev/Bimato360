<<<<<<< HEAD
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaErpPartnerViewSet

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

    path('<str:public_id>/tags/',
         BimaErpPartnerViewSet.as_view({'get': 'list_tags', 'post': 'create_tag'}),
         name='partner-tags'),
    path('<str:public_id>/tags/<str:entity_tag_public_id>/',
         BimaErpPartnerViewSet.as_view({'get': 'get_tag'}),
         name='partner-get-tag'),

    path('<str:public_id>/bank_account/',
         BimaErpPartnerViewSet.as_view({'get': 'list_bank_account', 'post': 'create_bank_account'}),
         name='partner-bank_accounts'),
    path('<str:public_id>/bank_account/<str:bank_account_public_id>/',
         BimaErpPartnerViewSet.as_view({'get': 'get_bank_account'}),
         name='partner-bank_account'),
]
=======
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaErpPartnerViewSet

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

    path('<str:public_id>/tags/',
         BimaErpPartnerViewSet.as_view({'get': 'list_tags', 'post': 'create_tag'}),
         name='partner-tags'),
    path('<str:public_id>/tags/<str:entity_tag_public_id>/',
         BimaErpPartnerViewSet.as_view({'get': 'get_tag'}),
         name='partner-get-tag'),

    path('<str:public_id>/bank_account/',
         BimaErpPartnerViewSet.as_view({'get': 'list_bank_account', 'post': 'create_bank_account'}),
         name='partner-bank_accounts'),
    path('<str:public_id>/bank_account/<str:bank_account_public_id>/',
         BimaErpPartnerViewSet.as_view({'get': 'get_bank_account'}),
         name='partner-bank_account'),
]
>>>>>>> origin/ma-branch
