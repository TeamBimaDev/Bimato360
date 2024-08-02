

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaCoreNotificationViewSet

router = DefaultRouter()
router.register('', BimaCoreNotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


