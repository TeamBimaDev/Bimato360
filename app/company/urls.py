<<<<<<< HEAD
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaCompanyViewSet

router = DefaultRouter()
router.register('', BimaCompanyViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('<str:public_id>/documents/',
         BimaCompanyViewSet.as_view({'get': 'list_documents', 'post': 'create_document'}),
         name='company-documents'),
    path('<str:public_id>/documents/<str:document_public_id>/',
         BimaCompanyViewSet.as_view({'get': 'get_document'}),
         name='company-document'),

    path('<str:public_id>/bank_account/',
         BimaCompanyViewSet.as_view({'get': 'list_bank_account', 'post': 'create_bank_account'}),
         name='company-bank_accounts'),
    path('<str:public_id>/bank_account/<str:bank_account_public_id>/',
         BimaCompanyViewSet.as_view({'get': 'get_bank_account'}),
         name='company-bank_account'),
]
=======
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BimaCompanyViewSet

router = DefaultRouter()
router.register('', BimaCompanyViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('<str:public_id>/documents/',
         BimaCompanyViewSet.as_view({'get': 'list_documents', 'post': 'create_document'}),
         name='company-documents'),
    path('<str:public_id>/documents/<str:document_public_id>/',
         BimaCompanyViewSet.as_view({'get': 'get_document'}),
         name='company-document'),

    path('<str:public_id>/bank_account/',
         BimaCompanyViewSet.as_view({'get': 'list_bank_account', 'post': 'create_bank_account'}),
         name='company-bank_accounts'),
    path('<str:public_id>/bank_account/<str:bank_account_public_id>/',
         BimaCompanyViewSet.as_view({'get': 'get_bank_account'}),
         name='company-bank_account'),
]
>>>>>>> origin/ma-branch
