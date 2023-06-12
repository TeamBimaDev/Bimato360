from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaErpSaleDocumentViewSet

router = DefaultRouter()
router.register('', BimaErpSaleDocumentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]