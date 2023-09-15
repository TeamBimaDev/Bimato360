from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaCoreNotificationTemplateViewSet

router = DefaultRouter()
router.register('', BimaCoreNotificationTemplateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]