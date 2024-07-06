from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaHrSkillViewSet

router = DefaultRouter()

router.register('', BimaHrSkillViewSet)

urlpatterns = [
    path('', include(router.urls))
]
