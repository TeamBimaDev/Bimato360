
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaHrInterviewViewStepSet

router = DefaultRouter()
router.register('', BimaHrInterviewViewStepSet)

urlpatterns = [
    path('', include(router.urls)),
]
