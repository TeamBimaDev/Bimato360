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

    def prepare_questions(self, vacancie_public_id: str, candidat_public_id: str) -> Optional[float]:
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
                generate_questions_prompt = ChatPromptTemplate.from_template(
                    "Create an interview guideline and prepare a total of 8 technical questions. "
                    "These questions should assess the candidate's technical knowledge, problem-solving abilities, and expertise in relevant technologies. "
                    "Focus on the keywords from the candidate's resume: {resume_keywords}, and the job description: {job_description}. "
                    "The output must be only in JSON format, where each key is the question number and each value is the corresponding question."
                )

                resume_chain = resume_prompt | llm | StrOutputParser()
                generate_questions_chain = generate_questions_prompt | llm | StrOutputParser()

                resume_keywords = resume_chain.invoke({"resume": cv_content})
                questions_text = generate_questions_chain.invoke({"resume_keywords": resume_keywords, "job_description": vacancie_description})
                questions_json = self.extract_json(questions_text)
                return questions_json
                    
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

    def extract_json(self, text):
        start_index = text.find('{')
        end_index = text.rfind('}')
        if start_index != -1 and end_index != -1:
            text=  text[start_index:end_index+1]
            return  json.loads(text)
        else:
            return None

    @action(detail=True, methods=['POST'], url_path='generate_questions')
    def generate_questions(self, request, pk=None):
        try:
            interview = self.get_object()
            vacancie_public_id = interview.vacancie.public_id
            candidat_public_id = interview.candidat.public_id 
            questions = self.prepare_questions(vacancie_public_id, candidat_public_id)

            if not questions:
                return Response({"status": "No questions generated."}, status=status.HTTP_400_BAD_REQUEST)

            for number, question_text in questions.items():
                question_instance = BimaHrInterviewQuestion(
                    question=question_text,
                    interview=interview
                )
                question_instance.save()
            
            return Response({"status": "Questions generated and saved successfully."}, status=status.HTTP_201_CREATED)
        
        except ValidationError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  