

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaCoreDepartmentViewSet

router = DefaultRouter()
router.register('', BimaCoreDepartmentViewSet)

urlpatterns = [
    path('', include(router.urls)),

]


