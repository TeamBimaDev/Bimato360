from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaTreasuryPaymentTermDetailViewSet

router = DefaultRouter()
router.register('', BimaTreasuryPaymentTermDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
