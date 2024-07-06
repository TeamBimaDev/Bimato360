from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaErpVatViewSet

router = DefaultRouter()
router.register('', BimaErpVatViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
