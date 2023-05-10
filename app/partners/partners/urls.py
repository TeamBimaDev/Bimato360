from django.urls import path, include
from rest_framework.routers import DefaultRouter
from partners.partners.views import BimaPartnersViewSet
router = DefaultRouter()
router.register('', BimaPartnersViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('<str:public_id>/addresses/', BimaPartnersViewSet.as_view({'get': 'list_addresses'}), name='partners-addresses'),
    path('<str:public_id>/ajoutaddress/', BimaPartnersViewSet.as_view({'post': 'ajout_address_for_partners'}), name='ajout-address-partners'),
    path('<str:public_id>/document/', BimaPartnersViewSet.as_view({'get': 'list_documents'}), name='document-partners'),
    path('<str:public_id>/ajoutdocument/', BimaPartnersViewSet.as_view({'post': 'ajout_document_for_partners'},name ='ajout-document-partners')),
    path('<str:public_id>/contact/', BimaPartnersViewSet.as_view({'get': 'list_contact'}), name='document-partners'),
    path('<str:public_id>/ajoutcontact/',BimaPartnersViewSet.as_view({'post':'ajout_contact_for_partners'},name ='ajout-contact-partners')),
]