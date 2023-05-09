from django.urls import path, include
from rest_framework.routers import DefaultRouter
from company.views import BimaCompanyViewSet

router = DefaultRouter()
router.register('', BimaCompanyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<str:public_id>/addresses/', BimaCompanyViewSet.as_view({'get': 'list_addresses'}),
         name='company-addresses'),
]