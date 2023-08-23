from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaTreasuryTransactionViewSet

router = DefaultRouter()
router.register('', BimaTreasuryTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<str:public_id>/tags/',
         BimaTreasuryTransactionViewSet.as_view({'get': 'list_tags', 'post': 'create_tag'}),
         name='transaction-tags'),
    path('<str:public_id>/tags/<str:entity_tag_public_id>/',
         BimaTreasuryTransactionViewSet.as_view({'get': 'get_tag'}),
         name='transaction-get-tag'),
]
