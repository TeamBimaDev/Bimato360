
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from hr.applicant.views import BimaHrApplicantViewSet

router = DefaultRouter()
router.register('', BimaHrApplicantViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<str:public_id>/addresses/', BimaHrApplicantViewSet.as_view({'get': 'list_addresses'}), name='applicant-addresses'),
    path('<str:public_id>/contacts/', BimaHrApplicantViewSet.as_view({'get': 'list_contacts'}), name='applicant-contacts'),
    path('<str:public_id>/interviews/', BimaHrApplicantViewSet.as_view({'get': 'list_interviews'}), name='applicant-interviews'),
    path('<str:public_id>/entity_tag/', BimaHrApplicantViewSet.as_view({'get': 'list_tags'}), name='applicant-entity_tag'),
    path('<str:public_id>/refuse/', BimaHrApplicantViewSet.as_view({'get': 'list_refuse'}), name='applicant-refuse'),
    path('<str:public_id>/documents/', BimaHrApplicantViewSet.as_view({'get': 'list_documents'}), name='applicant-documents'),
    path('<str:public_id>/skills/', BimaHrApplicantViewSet.as_view({'get': 'list_skills'}), name='applicant-skills'),
    path('<str:public_id>/activities/', BimaHrApplicantViewSet.as_view({'get': 'list_activities'}), name='applicant-activities'),
]
