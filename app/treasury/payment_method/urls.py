from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaTreasuryPaymentMethodViewSet

router = DefaultRouter()
router.register('', BimaTreasuryPaymentMethodViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
