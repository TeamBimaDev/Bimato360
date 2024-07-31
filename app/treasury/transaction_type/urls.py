<<<<<<< HEAD
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaTreasuryTransactionTypeViewSet

router = DefaultRouter()
router.register('', BimaTreasuryTransactionTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
=======
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaTreasuryTransactionTypeViewSet

router = DefaultRouter()
router.register('', BimaTreasuryTransactionTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
>>>>>>> origin/ma-branch
