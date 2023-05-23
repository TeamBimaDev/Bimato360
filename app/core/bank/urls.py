from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCoreBankViewSet

router = DefaultRouter()
router.register('', BimaCoreBankViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<str:public_id>/addresses/', BimaCoreBankViewSet.as_view({'get': 'list_addresses'}), name='bank-addresses'),
    path('<str:public_id>/add_address/', BimaCoreBankViewSet.as_view({'post': 'add_address_for_bank'}), name='ajout-address-bank'),
]
