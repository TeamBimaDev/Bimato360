from django.urls import path, include
from hr.applicant.views import BimaHrApplicantViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', BimaHrApplicantViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('<str:public_id>/documents/',
         BimaHrApplicantViewSet.as_view({'get': 'list_documents', 'post': 'create_document'}),
         name='applicant-documents'),
    path('<str:public_id>/documents/<str:document_public_id>/',
         BimaHrApplicantViewSet.as_view({'get': 'get_document'}),
         name='applicant-document'),

    path('<str:public_id>/bank_accounts/',
         BimaHrApplicantViewSet.as_view({'get': 'list_bank_account', 'post': 'create_bank_account'}),
         name='applicant-bank_accounts'),
    path('<str:public_id>/bank_accounts/<str:bank_account_public_id>/',
         BimaHrApplicantViewSet.as_view({'get': 'get_bank_account'}),
         name='applicant-bank_account'),

    path('<str:public_id>/addresses/',
         BimaHrApplicantViewSet.as_view({'get': 'list_addresses', 'post': 'create_address'}),
         name='applicant-addresses'),
    path('<str:public_id>/addresses/<str:contact_public_id>/',
         BimaHrApplicantViewSet.as_view({'get': 'get_address'}),
         name='applicant-addresses'),

    path('<str:public_id>/contacts/',
         BimaHrApplicantViewSet.as_view({'get': 'list_contacts', 'post': 'create_contact'}),
         name='applicant-contacts'),
    path('<str:public_id>/contacts/<str:contact_public_id>/',
         BimaHrApplicantViewSet.as_view({'get': 'get_contact'}),
         name='applicant-contact'),
]
