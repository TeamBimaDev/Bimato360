from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaHrVacancieViewSet

router = DefaultRouter()
router.register('', BimaHrVacancieViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
