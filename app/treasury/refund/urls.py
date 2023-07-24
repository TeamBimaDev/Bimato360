from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaTreasuryRefundViewSet

router = DefaultRouter()
router.register('', BimaTreasuryRefundViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<str:public_id>/bimatreasurytransaction/', BimaTreasuryTransactionViewSet.as_view({'get': 'get_bimatreasurytransaction_by_bimatreasuryrefund'}), name='Bimatreasurytransaction-By-BimaTreasuryRefund'),
]
