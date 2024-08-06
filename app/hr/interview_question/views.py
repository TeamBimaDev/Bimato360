import django_filters
from common.converters.default_converters import str_to_bool
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BimaHrInterviewQuestion
from .serializers import BimaHrInterviewQuestionSerializer



class BimaHrInterviewQuestionViewSet(AbstractViewSet):
    queryset = BimaHrInterviewQuestion.objects.all()
    serializer_class = BimaHrInterviewQuestionSerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        'list': ['interview_question.can_read'],
        'create': ['interview_question.can_create'],
        'retrieve': ['interview_question.can_read'],
        'update': ['interview_question.can_update'],
        'partial_update': ['interview_question.can_update'],
        'destroy': ['interview_question.can_delete'],
    }

    def get_object(self):
        obj = BimaHrInterviewQuestion.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
    


        

