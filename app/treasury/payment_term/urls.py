from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaTreasuryPaymentTermViewSet

router = DefaultRouter()
router.register('', BimaTreasuryPaymentTermViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
