from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCoreTagsViewSet

router = DefaultRouter()
router.register('', BimaCoreTagsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
