from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCompanyViewSet

router = DefaultRouter()
router.register('', BimaCompanyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<str:public_id>/addresses/', BimaCompanyViewSet.as_view({'get': 'list_addresses'}), name='company-addresses'),
    path('<str:public_id>/ajoutaddress/', BimaCompanyViewSet.as_view({'get': 'ajout_address_for_company'}), name='ajout-address-company'),
    path('<str:public_id>/document/', BimaCompanyViewSet.as_view({'get': 'list_documents'}), name='document-addresses'),
    path('<str:public_id>/ajoutdocument/', BimaCompanyViewSet.as_view({'get': 'ajout_document_for_company'}),
         name='ajout-document-company'),
]