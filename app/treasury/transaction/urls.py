from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaTreasuryTransactionViewSet

router = DefaultRouter()
router.register('', BimaTreasuryTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<str:public_id>/bimaerppartner/', BimaErpPartnerViewSet.as_view({'get': 'get_bimaerppartner_by_bimatreasurytransaction'}), name='Bimaerppartner-By-BimaTreasuryTransaction'),
]
