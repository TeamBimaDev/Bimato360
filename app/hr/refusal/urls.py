from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaHrRefuseViewSet

router = DefaultRouter()

router.register('', BimaHrRefuseViewSet)


urlpatterns = [
    path('',include(router.urls))
]