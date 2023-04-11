from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaHrCondidatPosteViewSet

router = DefaultRouter()

router.register('', BimaHrCondidatPosteViewSet)



urlpatterns = [
    path('',include(router.urls)),
]
