from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaErpCategoryViewSet

router = DefaultRouter()
router.register('', BimaErpCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
