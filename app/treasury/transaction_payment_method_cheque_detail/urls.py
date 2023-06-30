from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaTreasuryTransactionPaymentMethodChequeDetailViewSet

router = DefaultRouter()
router.register('', BimaTreasuryTransactionPaymentMethodChequeDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<str:public_id>/bimatreasurytransactionpaymentmethod/', BimaTreasuryTransactionPaymentMethodViewSet.as_view({'get': 'get_bimatreasurytransactionpaymentmethod_by_bimatreasurytransactionpaymentmethodchequedetail'}), name='Bimatreasurytransactionpaymentmethod-By-BimaTreasuryTransactionPaymentMethodChequeDetail'),
]
