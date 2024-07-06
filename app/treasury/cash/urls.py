from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaTreasuryCashViewSet

router = DefaultRouter()
router.register('', BimaTreasuryCashViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
