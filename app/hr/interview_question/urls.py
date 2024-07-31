from django.urls import path, include
from rest_framework.routers import DefaultRouter
from hr.interview_question.views import BimaHrInterviewQuestionViewSet

router = DefaultRouter()
router.register('', BimaHrInterviewQuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    ]