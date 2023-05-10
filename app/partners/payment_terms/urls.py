from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaPartnersPaymentViewSet

router = DefaultRouter()

router.register('', BimaPartnersPaymentViewSet)


urlpatterns = [
    path('',include(router.urls))
]