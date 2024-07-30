from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet

from .models import BimaHrInterviewStep
from .serializers import BimaHrInterviewStepSerializer


class BimaHrInterviewViewStepSet(AbstractViewSet):
    queryset = BimaHrInterviewStep.objects.all()
    serializer_class = BimaHrInterviewStepSerializer
    permission_classes = []
    #permission_classes = (ActionBasedPermission,)
    action_permissions = {
        'list': ['interview_step.can_read'],
        'create': ['interview_step.can_create'],
        'retrieve': ['interview_step.can_read'],
        'update': ['interview_step.can_update'],
        'partial_update': ['interview_step.can_update'],
        'destroy': ['interview_step.can_delete'],
    }

    def get_object(self):
        obj = BimaHrInterviewStep.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
