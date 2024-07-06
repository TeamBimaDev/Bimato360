from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCoreBankViewSet

router = DefaultRouter()
router.register('', BimaCoreBankViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('<str:public_id>/addresses/',
         BimaCoreBankViewSet.as_view({'get': 'list_addresses', 'post': 'create_address'}),
         name='bank-addresses'),
    path('<str:public_id>/addresses/<str:address_public_id>/',
         BimaCoreBankViewSet.as_view({'get': 'get_address'}),
         name='bank-get-address'),
]
