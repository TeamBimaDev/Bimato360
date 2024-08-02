from rest_framework.response import Response
from hr.vacancie.serializers import BimaHrCandidatVacancieSerializer
from hr.vacancie.models import BimaHrCandidatVacancie
from hr.employee.models import BimaHrEmployee
from core.abstract.views import AbstractViewSet
from .models import BimaHrTechnicalInterview,BimaHrEmployeeinterviewer
from .serializers import BimaHrTechnicalInterviewSerializer
from .filters import  BimaHrTechnicalInterviewFilter
from hr.vacancie.models import BimaHrVacancie
from hr.interview_question.models import BimaHrInterviewQuestion
from rest_framework.decorators import action
from rest_framework import status
from common.enums.interview import get_interview_status_choices
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from django.http import Http404
from typing import Optional
from django.shortcuts import get_object_or_404
from core.document.models import  get_documents_for_parent_entity
from django.core.files.storage import default_storage
from hr.candidat.models import BimaHrCandidat
from rest_framework.exceptions import ValidationError
from common.permissions.action_base_permission import ActionBasedPermission
import logging 
import fitz 
import json



logger = logging.getLogger(__name__)


class BimaHrTechnicalInterviewViewSet(AbstractViewSet):
    queryset = BimaHrTechnicalInterview.objects.all()
    serializer_class = BimaHrTechnicalInterviewSerializer
    filterset_class = BimaHrTechnicalInterviewFilter
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        'list': ['technical_interview.can_read'],
        'create': ['technical_interview.can_create'],
        'retrieve': ['technical_interview.can_read'],
        'update': ['technical_interview.can_update'],
        'partial_update': ['technical_interview.can_update'],
        'destroy': ['technical_interview.can_delete'],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger

    def get_object(self):
        obj = BimaHrTechnicalInterview.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj  
        

    
  