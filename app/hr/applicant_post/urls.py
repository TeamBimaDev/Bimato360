from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaHrApplicantPostViewSet

router = DefaultRouter()

router.register('', BimaHrApplicantPostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
