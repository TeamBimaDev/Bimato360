from django.urls import path, include
from rest_framework.routers import DefaultRouter
from hr.Te_interview_question.views import BimaHrTechnicalInterviewQuestionViewSet

router = DefaultRouter()
router.register('', BimaHrTechnicalInterviewQuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    ]