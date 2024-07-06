from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCoreTagViewSet

router = DefaultRouter()
router.register('', BimaCoreTagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
