from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCoreCurrencyViewSet

router = DefaultRouter()
router.register('', BimaCoreCurrencyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
