<<<<<<< HEAD
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaTreasuryBankAccountViewSet

router = DefaultRouter()
router.register('', BimaTreasuryBankAccountViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
=======
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaTreasuryBankAccountViewSet

router = DefaultRouter()
router.register('', BimaTreasuryBankAccountViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
>>>>>>> origin/ma-branch
