from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaHrActivityViewSet

router = DefaultRouter()

router.register('', BimaHrActivityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<str:public_id>/documents/',
         BimaHrActivityViewSet.as_view({'get': 'list_documents', 'post': 'create_document'}),
         name='activity-documents'),
    path('<str:public_id>/documents/<str:document_public_id>/',
         BimaHrActivityViewSet.as_view({'get': 'get_document'}),
         name='activity-document'),
]
