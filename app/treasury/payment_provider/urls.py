from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaTreasuryPaymentProviderViewSet

router = DefaultRouter()
router.register('', BimaTreasuryPaymentProviderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]