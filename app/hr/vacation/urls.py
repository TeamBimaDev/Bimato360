from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaHrVacationViewSet

router = DefaultRouter()

router.register('', BimaHrVacationViewSet)

urlpatterns = [
    path('', include(router.urls))
]
