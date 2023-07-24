from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaTreasuryTransactionPaymentMethodViewSet

router = DefaultRouter()
router.register('', BimaTreasuryTransactionPaymentMethodViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
#     path('<str:public_id>/bimacorecash/', BimaCoreCashViewSet.as_view({'get': 'get_bimacorecash_by_bimatreasurytransactionpaymentmethod'}), name='Bimacorecash-By-BimaTreasuryTransactionPaymentMethod'),
#     path('<str:public_id>/paymentmethod/', PaymentMethodViewSet.as_view({'get': 'get_paymentmethod_by_bimatreasurytransactionpaymentmethod'}), name='Paymentmethod-By-BimaTreasuryTransactionPaymentMethod'),
#     path('<str:public_id>/bimatreasurypaymentprovider/', BimaTreasuryPaymentProviderViewSet.as_view({'get': 'get_bimatreasurypaymentprovider_by_bimatreasurytransactionpaymentmethod'}), name='Bimatreasurypaymentprovider-By-BimaTreasuryTransactionPaymentMethod'),
#     path('<str:public_id>/bimatreasurytransaction/', BimaTreasuryTransactionViewSet.as_view({'get': 'get_bimatreasurytransaction_by_bimatreasurytransactionpaymentmethod'}), name='Bimatreasurytransaction-By-BimaTreasuryTransactionPaymentMethod'),
#     path('<str:public_id>/bimacorebank/', BimaCoreBankViewSet.as_view({'get': 'get_bimacorebank_by_bimatreasurytransactionpaymentmethod'}), name='Bimacorebank-By-BimaTreasuryTransactionPaymentMethod'),
# ]

urlpatterns = [
    path('', include(router.urls)),
]
