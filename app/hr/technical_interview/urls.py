
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaHrTechnicalInterviewViewSet

router = DefaultRouter()
router.register('', BimaHrTechnicalInterviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    ]
