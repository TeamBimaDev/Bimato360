from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaHrActivityViewSet

router = DefaultRouter()

router.register('', BimaHrActivityViewSet)



urlpatterns = [
    path('',include(router.urls)),
]
