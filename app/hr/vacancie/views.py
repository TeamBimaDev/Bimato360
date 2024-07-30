from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import re
from django.http import Http404

import logging
from typing import Optional
from core.document.models import BimaCoreDocument, get_documents_for_parent_entity
from django.core.files.storage import default_storage



from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet

from .filters import BimaHrVacancieFilter
from .models import BimaHrVacancie
from .serializers import BimaHrVacancieSerializer


from core.abstract.views import AbstractViewSet

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _


from hr.vacancie.models import BimaHrVacancie
from .serializers import BimaHrCandidatVacancieSerializer
from .models import BimaHrVacancie, BimaHrCandidatVacancie
from hr.candidat.models import BimaHrCandidat
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
import fitz

logger = logging.getLogger(__name__)



class BimaHrVacancieViewSet(AbstractViewSet):
    queryset = BimaHrVacancie.objects.select_related('department', 'job_category', 'manager').all()
    serializer_class = BimaHrVacancieSerializer
    ordering = ["-title"]
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    ordering_fields = ['title', 'department__name']
    filterset_class = BimaHrVacancieFilter

    action_permissions = {
        'list': ['vacancie.can_read'],
        'create': ['vacancie.can_create'],
        'retrieve': ['vacancie.can_read'],
        'update': ['vacancie.can_update'],
        'partial_update': ['vacancie.can_update'],
        'destroy': ['vacancie.can_delete'],
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger

    def calculate_score(self, vacancie_public_id: str, candidat_public_id: str) -> Optional[float]:
        try:
            llm = ChatOllama(model="llama3", temperature=0.01)
        except Exception as e:
            self.logger.error(f"Failed to initialize LLM: {e}")
            return None

        try:
            self.logger.debug(f"Trying to fetch vacancie with public ID: {vacancie_public_id}")
            vacancie = get_object_or_404(BimaHrVacancie, public_id=vacancie_public_id)
            vacancie_description = vacancie.description
            self.logger.debug(f"Vacancie fetched successfully: {vacancie}")
        except Http404:
            self.logger.error(f"Vacancie with public ID {vacancie_public_id} not found.")
            return None

          
        cv_content = self.read_pdf_content(candidat_public_id)
        if cv_content is not None:
            try:
                resume_prompt = ChatPromptTemplate.from_template(
                    "From this resume: {resume}, extract the keywords that are most relevant to identifying the candidate’s qualifications and expertise. Focus on specific skills, technologies, certifications, job titles, and significant achievements. These keywords should help recruiters quickly understand the candidate’s skills and experiences."
                )
                score_prompt = ChatPromptTemplate.from_template(
                    "Evaluate the compatibility of the candidate with the job offer by generating a score between 0 and 100. To determine this score, compare the candidate's resume keywords: {resume_keywords} with the job description: {job_description}. Consider the following factors: relevance of skills, technologies, job titles, qualifications, and key responsibilities. A higher score indicates a better match. Display the final score as a number between dashes, for example, --50--."
                )

                resume_chain = resume_prompt | llm | StrOutputParser()
                score_chain = score_prompt | llm | StrOutputParser()

                resume_keywords = resume_chain.invoke({"resume": cv_content})
                score_interpretation = score_chain.invoke({"resume_keywords": resume_keywords, "job_description": vacancie_description})

                score = self.extract_score(score_interpretation)
                return score
                    
            except Exception as e:
                self.logger.error(f"Failed to invoke LLM or parse output: {e}")
                return None
        else:
            return None

    def read_pdf_content(self, candidat_public_id):
        try:
            candidat = BimaHrCandidat.objects.get_object_by_public_id(candidat_public_id)
            documents = get_documents_for_parent_entity(candidat)

            cv_candidat = get_object_or_404(
                documents,
                file_type='CANDIDAT_CV')

            file_pdf = default_storage.path(str(cv_candidat.file_path))
            doc = fitz.open(file_pdf)
            pdf_text = ""
            for page in doc:
                pdf_text += page.get_text()
            return pdf_text

        except Exception as e:
            self.logger.error(f"An error occurred while reading the PDF: {e}")
            return None

    def extract_score(self, text):
        match = re.search(r'--(\d{1,3})--', text)
        if match:
            return int(match.group(1))
        else:
            return None

    @action(detail=True, methods=['GET'], url_path='candidat_applied')
    def candidat_applied(self, request, pk=None):
        vacancie = self.get_object()
        candidat_vacancie = BimaHrCandidatVacancie.objects.filter(vacancie=vacancie)
        serializer = BimaHrCandidatVacancieSerializer(candidat_vacancie, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'], url_path='add_candidat')
    def add_candidat(self, request, pk=None):
        vacancie = self.get_object()
        data = request.data.copy()
        candidat_public_id = data.get('candidat_public_id')
        data['vacancie_public_id'] = vacancie.public_id 
        score = self.calculate_score(vacancie.public_id, candidat_public_id)
        data['score'] = score
        serializer = BimaHrCandidatVacancieSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['DELETE'], url_path='delete-candidat/(?P<candidat_vacancie_public_id>[^/.]+)')
    def delete_candidat(self, request, pk=None):
        candidat_vacancie_public_id = request.data.get('candidat_vacancie_public_id')
        try:
            vacancie_post = BimaHrCandidatVacancie.objects.get(public_id=candidat_vacancie_public_id)
            vacancie_post.delete()
            return Response({"detail": "Vacancie application deleted."}, status=status.HTTP_204_NO_CONTENT)
        except BimaHrCandidatVacancie.DoesNotExist:
            return Response({"detail": "Vacancie not found."}, status=status.HTTP_404_NOT_FOUND)

    def get_object(self):
        obj = BimaHrVacancie.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
