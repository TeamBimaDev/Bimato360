from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCoreDocumentViewSet

router = DefaultRouter()
router.register('', BimaCoreDocumentViewSet)


urlpatterns = [
    path('list_file_type_partner/',
         BimaCoreDocumentViewSet.as_view({'get': 'get_list_file_type_partner'}),
         name='list_file_type_partner'),
    path('<str:public_id>/download/',
         BimaCoreDocumentViewSet.as_view({'get': 'download_file'}),
         name='download_file'),
    path('', include(router.urls)),
]
