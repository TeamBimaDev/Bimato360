from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaAnalysisViewSet

router = DefaultRouter()

router.register('', BimaAnalysisViewSet, basename='analysis')

urlpatterns = [
    path('', include(router.urls)),
]
