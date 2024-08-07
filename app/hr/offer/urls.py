'''from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaHrOffreViewSet

router = DefaultRouter()
router.register('', BimaHrOffreViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('create-offre/', BimaHrOffreViewSet.as_view({'post': 'create_offre'}), name='create-offre'),
    path('<int:pk>/generate-description/', BimaHrOffreViewSet.as_view({'post': 'generate_description'}), name='generate-description'),
    path('<int:pk>/read-offre/', BimaHrOffreViewSet.as_view({'get': 'read_offre'}), name='read-offre'),
    path('<int:pk>/update-offre/', BimaHrOffreViewSet.as_view({'put': 'update_offre'}), name='update-offre'),
    path('<int:pk>/delete-offre/', BimaHrOffreViewSet.as_view({'delete': 'delete_offre'}), name='delete-offre'),
    path('list-offres/', BimaHrOffreViewSet.as_view({'get': 'list_bimahr_offres'}), name='list-offres')
]'''

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaHrOffreViewSet

router = DefaultRouter()
router.register('', BimaHrOffreViewSet)

urlpatterns = [
    path('', include(router.urls)),  
]