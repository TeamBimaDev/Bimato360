<<<<<<< HEAD
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCoreStateViewSet

router = DefaultRouter()
router.register('', BimaCoreStateViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
=======
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCoreStateViewSet

router = DefaultRouter()
router.register('', BimaCoreStateViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
>>>>>>> origin/ma-branch
