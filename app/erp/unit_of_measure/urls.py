

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaErpUnitOfMeasureViewSet

router = DefaultRouter()
router.register('', BimaErpUnitOfMeasureViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


