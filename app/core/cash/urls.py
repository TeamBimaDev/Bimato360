from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCoreCashViewSet

router = DefaultRouter()
router.register('', BimaCoreCashViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
