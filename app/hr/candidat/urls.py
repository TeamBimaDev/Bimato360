from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaHrCandidatViewSet

router = DefaultRouter()
router.register('', BimaHrCandidatViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('<str:public_id>/documents/',
         BimaHrCandidatViewSet.as_view({'get': 'list_documents', 'post': 'create_document'}),
         name='candidat-documents'),
    path('<str:public_id>/documents/<str:document_public_id>/',
         BimaHrCandidatViewSet.as_view({'get': 'get_document'}),
         name='candidat-document'),

    path('<str:public_id>/addresses/',
         BimaHrCandidatViewSet.as_view({'get': 'list_addresses', 'post': 'create_address'}),
         name='candidat-addresses'),
    path('<str:public_id>/addresses/<str:contact_public_id>/',
         BimaHrCandidatViewSet.as_view({'get': 'get_address'}),
         name='candidat-addresses'),

    path('<str:public_id>/contacts/',
         BimaHrCandidatViewSet.as_view({'get': 'list_contacts', 'post': 'create_contact'}),
         name='candidat-contacts'),
    path('<str:public_id>/contacts/<str:contact_public_id>/',
         BimaHrCandidatViewSet.as_view({'get': 'get_contact'}),
         name='candidat-contact'),

]

