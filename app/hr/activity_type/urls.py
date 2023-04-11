from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaHrActivityTypeViewSet

router = DefaultRouter()

router.register('',BimaHrActivityTypeViewSet)


urlpatterns = [
    path('',include(router.urls))
]