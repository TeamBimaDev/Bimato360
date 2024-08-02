

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCoreSourceViewSet

router = DefaultRouter()
router.register('', BimaCoreSourceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


