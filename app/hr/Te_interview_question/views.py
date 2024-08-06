import django_filters
from common.converters.default_converters import str_to_bool
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BimaHrTechnicalInterviewQuestion
from .serializers import BimaHrTechnicalInterviewQuestionSerializer



class BimaHrTechnicalInterviewQuestionViewSet(AbstractViewSet):
    queryset = BimaHrTechnicalInterviewQuestion.objects.all()
    serializer_class = BimaHrTechnicalInterviewQuestionSerializer
    permission_classes = []
    #permission_classes = (ActionBasedPermission,)
    action_permissions = {
        'list': ['interview_te_question.can_read'],
        'create': ['interview_te_question.can_create'],
        'retrieve': ['interview_te_question.can_read'],
        'update': ['interview_te_question.can_update'],
        'partial_update': ['interview_te_question.can_update'],
        'destroy': ['interview_te_question.can_delete'],
    }

    def get_object(self):
        obj = BimaHrTechnicalInterviewQuestion.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
    


        

