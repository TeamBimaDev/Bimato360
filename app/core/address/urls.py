from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCoreAddressViewSet

router = DefaultRouter()
router.register('', BimaCoreAddressViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
