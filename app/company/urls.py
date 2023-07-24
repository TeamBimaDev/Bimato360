from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCompanyViewSet

router = DefaultRouter()
router.register('', BimaCompanyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
