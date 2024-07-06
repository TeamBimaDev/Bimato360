from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaHrQuestionViewSet

router = DefaultRouter()

router.register('', BimaHrQuestionViewSet)

urlpatterns = [
    path('', include(router.urls))
]