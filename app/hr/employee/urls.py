from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaHrEmployeeViewSet

router = DefaultRouter()
router.register('', BimaHrEmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('<str:public_id>/documents/',
         BimaHrEmployeeViewSet.as_view({'get': 'list_documents', 'post': 'create_document'}),
         name='employee-documents'),
    path('<str:public_id>/documents/<str:document_public_id>/',
         BimaHrEmployeeViewSet.as_view({'get': 'get_document'}),
         name='employee-document'),

    path('<str:public_id>/bank_accounts/',
         BimaHrEmployeeViewSet.as_view({'get': 'list_bank_account', 'post': 'create_bank_account'}),
         name='employee-bank_accounts'),
    path('<str:public_id>/bank_accounts/<str:bank_account_public_id>/',
         BimaHrEmployeeViewSet.as_view({'get': 'get_bank_account'}),
         name='employee-bank_account'),

    path('<str:public_id>/addresses/',
         BimaHrEmployeeViewSet.as_view({'get': 'list_addresses', 'post': 'create_address'}),
         name='employee-addresses'),
    path('<str:public_id>/addresses/<str:contact_public_id>/',
         BimaHrEmployeeViewSet.as_view({'get': 'get_address'}),
         name='employee-addresses'),

    path('<str:public_id>/contacts/',
         BimaHrEmployeeViewSet.as_view({'get': 'list_contacts', 'post': 'create_contact'}),
         name='employee-contacts'),
    path('<str:public_id>/contacts/<str:contact_public_id>/',
         BimaHrEmployeeViewSet.as_view({'get': 'get_contact'}),
         name='employee-contact'),
]
