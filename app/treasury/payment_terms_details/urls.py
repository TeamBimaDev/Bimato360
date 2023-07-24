from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaTreasuryPaymentTermsDetailsViewSet

router = DefaultRouter()
router.register('', BimaTreasuryPaymentTermsDetailsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<str:public_id>/bimatreasurypaymentterms/', BimaTreasuryPaymentTermsViewSet.as_view({'get': 'get_bimatreasurypaymentterms_by_bimatreasurypaymenttermsdetails'}), name='Bimatreasurypaymentterms-By-BimaTreasuryPaymentTermsDetails'),
]
