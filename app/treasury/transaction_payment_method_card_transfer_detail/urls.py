from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaTreasuryTransactionPaymentMethodCardTransferDetailViewSet

router = DefaultRouter()
router.register('', BimaTreasuryTransactionPaymentMethodCardTransferDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
