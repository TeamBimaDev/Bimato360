from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaErpCategoryViewSet

router = DefaultRouter()
router.register('', BimaErpCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<str:public_id>/tags/',
         BimaErpCategoryViewSet.as_view({'get': 'list_tags', 'post': 'create_tag'}),
         name='category-tags'),
    path('<str:public_id>/tags/<str:entity_tag_public_id>/',
         BimaErpCategoryViewSet.as_view({'get': 'get_tag'}),
         name='category-get-tag'),
]
