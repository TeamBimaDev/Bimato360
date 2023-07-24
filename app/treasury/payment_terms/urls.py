from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaTreasuryPaymentTermsViewSet

router = DefaultRouter()
router.register('', BimaTreasuryPaymentTermsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
