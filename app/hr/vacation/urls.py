from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaHrVacationViewSet

router = DefaultRouter()

router.register('', BimaHrVacationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<str:public_id>/documents/',
         BimaHrVacationViewSet.as_view({'get': 'list_documents', 'post': 'create_document'}),
         name='vacation-documents'),
    path('<str:public_id>/documents/<str:document_public_id>/',
         BimaHrVacationViewSet.as_view({'get': 'get_document'}),
         name='vacation-document'),
]
