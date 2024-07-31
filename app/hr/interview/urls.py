<<<<<<< HEAD

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from hr.interview.views import BimaHrInterviewViewSet

router = DefaultRouter()
router.register('', BimaHrInterviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    ]
=======

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from hr.interview.views import BimaHrInterviewViewSet

router = DefaultRouter()
router.register('', BimaHrInterviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    ]
>>>>>>> origin/ma-branch
