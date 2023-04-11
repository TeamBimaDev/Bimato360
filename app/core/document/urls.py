from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCoreDocumentViewSet

router = DefaultRouter()
router.register('', BimaCoreDocumentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
