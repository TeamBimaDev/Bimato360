from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCoreSkillCategorViewSet

router = DefaultRouter()
router.register('', BimaCoreSkillCategorViewSet)


urlpatterns = [
    path('',include(router.urls))


]