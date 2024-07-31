<<<<<<< HEAD
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaErpProductViewSet

router = DefaultRouter()
router.register("", BimaErpProductViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "<str:public_id>/tags/",
        BimaErpProductViewSet.as_view({"get": "list_tags", "post": "create_tag"}),
        name="product-tags",
    ),
    path(
        "<str:public_id>/tags/<str:entity_tag_public_id>/",
        BimaErpProductViewSet.as_view({"get": "get_tag"}),
        name="product-get-tag",
    ),
]
=======
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaErpProductViewSet

router = DefaultRouter()
router.register("", BimaErpProductViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "<str:public_id>/tags/",
        BimaErpProductViewSet.as_view({"get": "list_tags", "post": "create_tag"}),
        name="product-tags",
    ),
    path(
        "<str:public_id>/tags/<str:entity_tag_public_id>/",
        BimaErpProductViewSet.as_view({"get": "get_tag"}),
        name="product-get-tag",
    ),
]
>>>>>>> origin/ma-branch
