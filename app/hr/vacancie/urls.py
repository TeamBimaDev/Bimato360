<<<<<<< HEAD
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaHrVacancieViewSet

router = DefaultRouter()
router.register('', BimaHrVacancieViewSet)


urlpatterns = [
    path('', include(router.urls)),
    
   # Route pour obtenir ou créer une offre spécifique pour une vacancie
    path('vacancie/<str:pk>/offers/', BimaHrVacancieViewSet.as_view({'get': 'offers', 'post': 'offers'}), name='vacancie-offers'),
    # Route pour obtenir une offre spécifique par son ID pour une vacancie
    path('vacancie/<str:pk>/offers/<str:offer_public_id>/', BimaHrVacancieViewSet.as_view({'get': 'get_offer'}), name='vacancie-offer'),

]

'''path('<str:public_id>/offers/<str:offer_public_id>/',
         BimaHrVacancieViewSet.as_view({'get': 'get_offer'}),
         name='vacancie-offer'),
    
    path('vacancie/<str:pk>/offers/', BimaHrVacancieViewSet.as_view({'get': 'offers', 'post': 'offers'}), name='vacancie-offers'),

    '''
=======
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaHrVacancieViewSet

router = DefaultRouter()
router.register('', BimaHrVacancieViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
>>>>>>> origin/ma-branch
