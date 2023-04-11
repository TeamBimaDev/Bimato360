from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCoreSkilllevelViewSet

router = DefaultRouter()

router.register('', BimaCoreSkilllevelViewSet )

urlpatterns = [
    path('',include(router.urls))

]