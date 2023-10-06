from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaHrContractViewSet

router = DefaultRouter()

router.register('', BimaHrContractViewSet)

urlpatterns = [
    path('', include(router.urls))
]
