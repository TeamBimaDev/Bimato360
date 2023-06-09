from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaCoreCountryViewSet

router = DefaultRouter()
router.register('', BimaCoreCountryViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('<str:public_id>/states/',
         BimaCoreCountryViewSet.as_view({'get': 'get_state_by_country'}),
         name='State-By-Country'),

    path('generate_pdf',
         BimaCoreCountryViewSet.as_view({'get': 'generate_pdf'}),
         name='generate_pdf'),

]
