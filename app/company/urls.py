from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCompanyViewSet

router = DefaultRouter()
router.register('', BimaCompanyViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('<str:public_id>/documents/',
         BimaCompanyViewSet.as_view({'get': 'list_documents', 'post': 'create_document'}),
         name='partner-documents'),
    path('<str:public_id>/documents/<str:document_public_id>/',
         BimaCompanyViewSet.as_view({'get': 'get_document'}),
         name='partner-document'),
]
