<<<<<<< HEAD
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCoreEntityTagViewSet

router = DefaultRouter()
router.register('', BimaCoreEntityTagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
=======
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCoreEntityTagViewSet

router = DefaultRouter()
router.register('', BimaCoreEntityTagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
>>>>>>> origin/ma-branch
