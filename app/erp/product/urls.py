from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaErpProductViewSet


router = DefaultRouter()
router.register('', BimaErpProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('export_csv',
         BimaErpProductViewSet.as_view({'get': 'export_data_csv'}),
         name='product-export_csv')
]
