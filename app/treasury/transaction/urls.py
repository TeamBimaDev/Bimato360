from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaTreasuryTransactionViewSet

router = DefaultRouter()
router.register('', BimaTreasuryTransactionViewSet)

urlpatterns = [
    path('', include(router.urls))
]
