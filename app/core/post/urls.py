from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCorePostViewSet

router = DefaultRouter()
router.register('', BimaCorePostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]