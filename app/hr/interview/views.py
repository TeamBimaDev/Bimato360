from rest_framework.response import Response
from hr.interview.filters import BimaHrInterviewFilter
from hr.vacancie.serializers import BimaHrCandidatVacancieSerializer
from hr.vacancie.models import BimaHrCandidatVacancie
from core.abstract.views import AbstractViewSet
from hr.interview.models import BimaHrInterview
from hr.interview.serializers import BimaHrInterviewSerializer
from rest_framework.decorators import action
from rest_framework import status
from common.enums.interview import get_interview_status_choices

class BimaHrInterviewViewSet(AbstractViewSet):
    queryset = BimaHrInterview.objects.all()
    serializer_class = BimaHrInterviewSerializer
    permission_classes = []
    ordering_fields = ['title', 'candidat__first_name']
    filterset_class = BimaHrInterviewFilter
    
    
    #permission_classes = (ActionBasedPermission,)
    action_permissions = {
        'list': ['interview.can_read'],
        'create': ['interview.can_create'],
        'retrieve': ['interview.can_read'],
        'update': ['interview.can_update'],
        'partial_update': ['interview.can_update'],
        'destroy': ['interview.can_delete'],
    }

    

    @action(detail=True, methods=['GET'], url_path='interview_applied')
    def interview_applied(self, request, pk=None):
        vacancie = self.get_object()
        candidat_vacancie = BimaHrCandidatVacancie.objects.filter(vacancie=vacancie)
        serializer = BimaHrCandidatVacancieSerializer(candidat_vacancie, many=True)
        return Response(serializer.data)
    
    

    
    @action(detail=True, methods=['post'], url_path='add_interview')
    def add_interview(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    @action(detail=True, methods=['delete'], url_path='delete-interview/(?P<candidat_vacancie_public_id>[^/.]+)')
    def delete_interview(self, request, pk=None, interview_public_id=None):
        try:
            interview_post = BimaHrInterview.objects.get(public_id=interview_public_id)
            interview_post.delete()
            return Response({"detail": "Interview application deleted."}, status=status.HTTP_204_NO_CONTENT)
        except BimaHrInterview.DoesNotExist:
            return Response({"detail": "Interview not found."}, status=status.HTTP_404_NOT_FOUND)
        
        
    @action(detail=False, methods=['get'], url_path='list_interview_status')
    def list_interview_status(self, request):
        formatted_response = {str(item[0]): str(item[1]) for item in get_interview_status_choices()}
        return Response(formatted_response)
   
    def get_object(self):
        obj = BimaHrInterview.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj  
    
    
    @action(detail=True, methods=['PUT'], url_path='update_interview')
    def update_interview(self, request, pk=None):
        interview = self.get_object()
        serializer = self.get_serializer(interview, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)