from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaUserRoleViewSet

router = DefaultRouter()
router.register('', BimaUserRoleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
