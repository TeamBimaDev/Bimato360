from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaTreasuryTransactionPaymentMethodBankTransferDetailViewSet

router = DefaultRouter()
router.register('', BimaTreasuryTransactionPaymentMethodBankTransferDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
