from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCoreCountryViewSet

router = DefaultRouter()
router.register('', BimaCoreCountryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
