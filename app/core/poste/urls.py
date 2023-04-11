from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCorePosteViewSet

router = DefaultRouter()
router.register('', BimaCorePosteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]