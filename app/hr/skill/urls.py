from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCoreSkillViewSet

router = DefaultRouter()

router.register('', BimaCoreSkillViewSet)


urlpatterns = [
    path('',include(router.urls))
]