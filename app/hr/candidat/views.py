<<<<<<< HEAD
import logging
from common.permissions.action_base_permission import ActionBasedPermission
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from core.abstract.views import AbstractViewSet
import re
from django.http import Http404

from typing import Optional

from django.core.files.storage import default_storage


from core.abstract.views import AbstractViewSet
from core.address.models import get_addresses_for_parent, create_single_address, BimaCoreAddress
from core.address.serializers import BimaCoreAddressSerializer
from core.contact.models import get_contacts_for_parent_entity, create_single_contact, BimaCoreContact
from core.contact.serializers import BimaCoreContactSerializer
from core.document.models import BimaCoreDocument, get_documents_for_parent_entity
from core.document.serializers import BimaCoreDocumentSerializer
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from hr.models import BimaHrPersonExperience
from hr.vacancie.models import BimaHrVacancie
from hr.serializers import BimaHrPersonSkillSerializer, BimaHrPersonExperienceSerializer
from hr.service import delete_person_experience, delete_person_skill, add_or_update_person_skill, \
    add_or_update_person_experience
from hr.skill.models import BimaHrPersonSkill
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from .filters import BimaHrCandidatFilter
from .models import BimaHrCandidat
from .serializers import BimaHrCandidatSerializer

logger = logging.getLogger(__name__)


class BimaHrCandidatViewSet(AbstractViewSet):
    queryset = BimaHrCandidat.objects.all()
    serializer_class = BimaHrCandidatSerializer
    ordering = ["-first_name"]
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    filterset_class = BimaHrCandidatFilter
    action_permissions = {
        'list': ['candidat.can_read'],
        'create': ['candidat.can_create'],
        'retrieve': ['candidat.can_read'],
        'update': ['candidat.can_update'],
        'partial_update': ['candidat.can_update'],
        'destroy': ['candidat.can_delete'],
        'documents': ['candidat.can_add_document'],
        'contacts': ['candidat.can_add_contact'],
        'addresses': ['candidat.can_add_address'],
        'delete_skill': ['candidat.can_manage_skill'],
        'add_update_skill': ['candidat.can_manage_skill'],
        'get_person_skills': ['candidat.can_manage_skill'],
        'delete_experience': ['candidat.can_manage_experience'],
        'get_skills': ['candidat.can_manage_skill'],
        'get_experiences': ['candidat.can_manage_experience'],

    }
    
    logger = logging.getLogger(__name__)
    
    
    
    def list_documents(self, request, *args, **kwargs):
        candidat = BimaHrCandidat.objects.get_object_by_public_id(self.kwargs['public_id'])
        documents = get_documents_for_parent_entity(candidat)
        serialized_document = BimaCoreDocumentSerializer(documents, many=True)
        return Response(serialized_document.data)

    def create_document(self, request, *args, **kwargs):
        candidat = BimaHrCandidat.objects.get_object_by_public_id(self.kwargs['public_id'])
        document_data = request.data
        document_data['file_path'] = request.FILES['file_path']
        result = BimaCoreDocument.create_document_for_parent(candidat, document_data)
        if isinstance(result, BimaCoreDocument):
            return Response({
                "id": result.public_id,
                "document_name": result.document_name,
                "description": result.description,
                "date_file": result.date_file,
                "file_type": result.file_type

            }, status=status.HTTP_201_CREATED)
        else:
            return Response(result, status=result.get("status", status.HTTP_500_INTERNAL_SERVER_ERROR))

    def get_document(self, request, *args, **kwargs):
        candidat = BimaHrCandidat.objects.get_object_by_public_id(self.kwargs['public_id'])
        document = get_object_or_404(BimaCoreDocument,
                                     public_id=self.kwargs['document_public_id'],
                                     parent_id=candidat.id)
        serialized_document = BimaCoreDocumentSerializer(document)
        return Response(serialized_document.data)

    def list_addresses(self, request, *args, **kwargs):
        candidat = BimaHrCandidat.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        addresses = get_addresses_for_parent(candidat)
        serialized_addresses = BimaCoreAddressSerializer(addresses, many=True)
        return Response(serialized_addresses.data)

    def create_address(self, request, *args, **kwargs):
        candidat = BimaHrCandidat.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        response = create_single_address(request.data, candidat)
        if "error" in response:
            return Response({"detail": response["error"]}, status=response["status"])
        return Response(response["data"], status=response["status"])

    def get_address(self, request, *args, **kwargs):
        candidat = BimaHrCandidat.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        address = get_object_or_404(
            BimaCoreAddress,
            public_id=self.kwargs["address_public_id"],
            parent_id=candidat.id,
        )
        serialized_address = BimaCoreAddressSerializer(address)
        return Response(serialized_address.data)

    def list_contacts(self, request, *args, **kwargs):
        candidat = BimaHrCandidat.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        contacts = get_contacts_for_parent_entity(candidat)
        serialized_contact = BimaCoreContactSerializer(contacts, many=True)
        return Response(serialized_contact.data)

    def create_contact(self, request, *args, **kwargs):
        candidat = BimaHrCandidat.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        response = create_single_contact(request.data, candidat)
        if "error" in response:
            return Response({"detail": response["error"]}, status=response["status"])
        return Response(response["data"], status=response["status"])

    def get_contact(self, request, *args, **kwargs):
        candidat = BimaHrCandidat.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        contact = get_object_or_404(
            BimaCoreContact,
            public_id=self.kwargs["contact_public_id"],
            parent_id=candidat.id,
        )
        serialized_contact = BimaCoreContactSerializer(contact)
        return Response(serialized_contact.data)

    @action(detail=True, methods=['POST'], url_path='add_update_skill')
    def add_update_skill(self, request, public_id=None):
        candidat = self.get_object()
        skill_public_id = request.data.get('skill_public_id')
        level = request.data.get('level')

        try:
            person_skill, created = add_or_update_person_skill(candidat, skill_public_id, level)
            if created:
                return Response({'status': 'Skill added'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'status': 'Skill updated'}, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response(e.detail, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['DELETE'], url_path='delete_skill')
    def delete_skill(self, request, public_id=None):
        candidat = self.get_object()
        skill_public_id = request.data.get('skill_public_id')

        try:
            delete_person_skill(candidat, skill_public_id)
            return Response({'status': 'Skill deleted'}, status=status.HTTP_204_NO_CONTENT)
        except NotFound as e:
            return Response(e.detail, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST', 'PUT'], url_path='add_update_experience')
    def add_update_experience(self, request, public_id=None):
        person = self.get_object()
        experience_data = request.data

        try:
            experience, created = add_or_update_person_experience(person, experience_data)
            if created:
                return Response({'status': 'Experience added', 'experience': experience},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'status': 'Experience updated', 'experience': experience},
                                status=status.HTTP_200_OK)
        except NotFound as e:
            return Response(e.detail, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['DELETE'], url_path='delete_experience')
    def delete_experience(self, request, public_id=None):
        person = self.get_object()
        experience_public_id = request.data.get('experience_public_id')

        try:
            delete_person_experience(person, experience_public_id)
            return Response({'status': 'Experience deleted'}, status=status.HTTP_204_NO_CONTENT)
        except NotFound as e:
            return Response(e.detail, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['GET'], url_path='get_skills')
    def get_skills(self, request, public_id=None):
        person = self.get_object()
        person_skills = BimaHrPersonSkill.objects.filter(person=person)
        serializer = BimaHrPersonSkillSerializer(person_skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'], url_path='get_experiences')
    def get_experiences(self, request, public_id=None):
        person = self.get_object()
        person_experiences = BimaHrPersonExperience.objects.filter(person=person)
        serializer = BimaHrPersonExperienceSerializer(person_experiences, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        obj = BimaHrCandidat.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj









'''

def calculate_score(self, vacancie_public_id: str, candidat_public_id: str) -> Optional[float]:
        try:
            llm = ChatOllama(model="llama3", temperature=0.01)
        except Exception as e:
            self.logger.error(f"Failed to initialize LLM: {e}")
            return None

        try:
            vacancie = get_object_or_404(BimaHrVacancie, public_id=vacancie_public_id)
            vacancie_description = vacancie.description
        except Http404:
            self.logger.error("Vacancie not found.")
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

            # Construct the file path using Django's default storage system
            file_pdf = default_storage.path(str(cv_candidat.file_path))
            print(file_pdf)
            # Open the file in binary mode
            with open(file_pdf, 'rb') as pdf_file:
                pdf_content = pdf_file.read()

            return pdf_content

        except Exception as e:
            self.logger.error(f"An error occurred while reading the PDF: {e}")
            return None

    def extract_score(self, text):
        match = re.search(r'--(\d{1,3})--', text)
        if match:
            return int(match.group(1))
        else:
            return None

    @action(detail=True, methods=['GET'], url_path='vacancie_applied')
    def vacancie_applied(self, request, pk=None):
        candidat = self.get_object()
        candidat_vacancie = candidat.candidat_vacancie.all()
        serializer = BimaHrCandidatVacancieSerializer(candidat_vacancie, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'], url_path='add_vacancie')
    def add_vacancie(self, request, pk=None):
        candidat = self.get_object()
        data = request.data.copy()
        vacancie_public_id = data.get('vacancie_public_id')
        data['candidat_public_id'] = candidat.public_id  # Ajouter l'ID du candidat aux données
        score = self.calculate_score(vacancie_public_id, candidat.public_id)
        data['score'] = score
        serializer = BimaHrCandidatVacancieSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   

    @action(detail=True, methods=['PUT'], url_path='update-vacancie/(?P<candidat_vacancie_public_id>[^/.]+)')
    def update_vacancie(self, request, pk=None):
        candidat_vacancie_public_id = request.data.get('candidat_vacancie_public_id')
        if not candidat_vacancie_public_id:
            raise ValidationError({'id': 'Vacancie post ID is required for update.'})

        try:
            vacancie_post = BimaHrCandidatVacancie.objects.get(public_id=candidat_vacancie_public_id)
        except BimaHrCandidatVacancie.DoesNotExist:
            return Response({"detail": "Vacancie not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BimaHrCandidatVacancieSerializer(vacancie_post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['DELETE'], url_path='delete-vacancie/(?P<candidat_vacancie_public_id>[^/.]+)')
    def delete_vacancie(self, request, pk=None):
        candidat_vacancie_public_id = request.data.get('candidat_vacancie_public_id')
        try:
            vacancie_post = BimaHrCandidatVacancie.objects.get(public_id=candidat_vacancie_public_id)
            vacancie_post.delete()
            return Response({"detail": "Vacancie application deleted."}, status=status.HTTP_204_NO_CONTENT)
        except BimaHrCandidatVacancie.DoesNotExist:
            return Response({"detail": "Vacancie not found."}, status=status.HTTP_404_NOT_FOUND)



'''









=======

import logging

from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet
from core.address.models import get_addresses_for_parent, create_single_address, BimaCoreAddress
from core.address.serializers import BimaCoreAddressSerializer
from core.contact.models import get_contacts_for_parent_entity, create_single_contact, BimaCoreContact
from core.contact.serializers import BimaCoreContactSerializer
from core.document.models import BimaCoreDocument, get_documents_for_parent_entity
from core.document.serializers import BimaCoreDocumentSerializer
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from hr.models import BimaHrPersonExperience
from hr.vacancie.models import BimaHrVacancie
from hr.serializers import BimaHrPersonSkillSerializer, BimaHrPersonExperienceSerializer
from hr.service import delete_person_experience, delete_person_skill, add_or_update_person_skill, \
    add_or_update_person_experience
from hr.skill.models import BimaHrPersonSkill
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from .filters import BimaHrCandidatFilter
from .models import BimaHrCandidat
from .serializers import BimaHrCandidatSerializer

logger = logging.getLogger(__name__)


class BimaHrCandidatViewSet(AbstractViewSet):
    queryset = BimaHrCandidat.objects.all()
    serializer_class = BimaHrCandidatSerializer
    ordering = ["-first_name"]
    permission_classes = []
    # permission_classes = (ActionBasedPermission,)
    filterset_class = BimaHrCandidatFilter
    action_permissions = {
        'list': ['candidat.can_read'],
        'create': ['candidat.can_create'],
        'retrieve': ['candidat.can_read'],
        'update': ['candidat.can_update'],
        'partial_update': ['candidat.can_update'],
        'destroy': ['candidat.can_delete'],
        'documents': ['candidat.can_add_document'],
        'contacts': ['candidat.can_add_contact'],
        'addresses': ['candidat.can_add_address'],
        'delete_skill': ['candidat.can_manage_skill'],
        'add_update_skill': ['candidat.can_manage_skill'],
        'get_person_skills': ['candidat.can_manage_skill'],
        'delete_experience': ['candidat.can_manage_experience'],
        'get_skills': ['candidat.can_manage_skill'],
        'get_experiences': ['candidat.can_manage_experience'],

    }
    
    logger = logging.getLogger(__name__)
    
    
    def list_documents(self, request, *args, **kwargs):
        candidat = BimaHrCandidat.objects.get_object_by_public_id(self.kwargs['public_id'])
        documents = get_documents_for_parent_entity(candidat)
        serialized_document = BimaCoreDocumentSerializer(documents, many=True)
        return Response(serialized_document.data)

    def create_document(self, request, *args, **kwargs):
        candidat = BimaHrCandidat.objects.get_object_by_public_id(self.kwargs['public_id'])
        document_data = request.data
        document_data['file_path'] = request.FILES['file_path']
        result = BimaCoreDocument.create_document_for_parent(candidat, document_data)
        if isinstance(result, BimaCoreDocument):
            return Response({
                "id": result.public_id,
                "document_name": result.document_name,
                "description": result.description,
                "date_file": result.date_file,
                "file_type": result.file_type

            }, status=status.HTTP_201_CREATED)
        else:
            return Response(result, status=result.get("status", status.HTTP_500_INTERNAL_SERVER_ERROR))

    def get_document(self, request, *args, **kwargs):
        candidat = BimaHrCandidat.objects.get_object_by_public_id(self.kwargs['public_id'])
        document = get_object_or_404(BimaCoreDocument,
                                     public_id=self.kwargs['document_public_id'],
                                     parent_id=candidat.id)
        serialized_document = BimaCoreDocumentSerializer(document)
        return Response(serialized_document.data)

    def list_addresses(self, request, *args, **kwargs):
        candidat = BimaHrCandidat.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        addresses = get_addresses_for_parent(candidat)
        serialized_addresses = BimaCoreAddressSerializer(addresses, many=True)
        return Response(serialized_addresses.data)

    def create_address(self, request, *args, **kwargs):
        candidat = BimaHrCandidat.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        response = create_single_address(request.data, candidat)
        if "error" in response:
            return Response({"detail": response["error"]}, status=response["status"])
        return Response(response["data"], status=response["status"])

    def get_address(self, request, *args, **kwargs):
        candidat = BimaHrCandidat.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        address = get_object_or_404(
            BimaCoreAddress,
            public_id=self.kwargs["address_public_id"],
            parent_id=candidat.id,
        )
        serialized_address = BimaCoreAddressSerializer(address)
        return Response(serialized_address.data)

    def list_contacts(self, request, *args, **kwargs):
        candidat = BimaHrCandidat.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        contacts = get_contacts_for_parent_entity(candidat)
        serialized_contact = BimaCoreContactSerializer(contacts, many=True)
        return Response(serialized_contact.data)

    def create_contact(self, request, *args, **kwargs):
        candidat = BimaHrCandidat.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        response = create_single_contact(request.data, candidat)
        if "error" in response:
            return Response({"detail": response["error"]}, status=response["status"])
        return Response(response["data"], status=response["status"])

    def get_contact(self, request, *args, **kwargs):
        candidat = BimaHrCandidat.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        contact = get_object_or_404(
            BimaCoreContact,
            public_id=self.kwargs["contact_public_id"],
            parent_id=candidat.id,
        )
        serialized_contact = BimaCoreContactSerializer(contact)
        return Response(serialized_contact.data)

    @action(detail=True, methods=['POST'], url_path='add_update_skill')
    def add_update_skill(self, request, pk=None):
        candidat = self.get_object()
        skill_public_id = request.data.get('skill_public_id')
        level = request.data.get('level')

        try:
            person_skill, created = add_or_update_person_skill(candidat, skill_public_id, level)
            if created:
                return Response({'status': 'Skill added'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'status': 'Skill updated'}, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response(e.detail, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['DELETE'], url_path='delete_skill')
    def delete_skill(self, request, pk=None):
        candidat = self.get_object()
        skill_public_id = request.data.get('skill_public_id')

        try:
            delete_person_skill(candidat, skill_public_id)
            return Response({'status': 'Skill deleted'}, status=status.HTTP_204_NO_CONTENT)
        except NotFound as e:
            return Response(e.detail, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST', 'PUT'], url_path='add_update_experience')
    def add_update_experience(self, request, pk=None):
        candidat = self.get_object()
        print(candidat)
        experience_data = request.data

        try:
            experience, created = add_or_update_person_experience(candidat, experience_data)
            if created:
                return Response({'status': 'Experience added', 'experience': experience},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'status': 'Experience updated', 'experience': experience},
                                status=status.HTTP_200_OK)
        except NotFound as e:
            return Response(e.detail, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['DELETE'], url_path='delete_experience')
    def delete_experience(self, request, pk=None):
        person = self.get_object()
        experience_public_id = request.data.get('experience_public_id')

        try:
            delete_person_experience(person, experience_public_id)
            return Response({'status': 'Experience deleted'}, status=status.HTTP_204_NO_CONTENT)
        except NotFound as e:
            return Response(e.detail, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['GET'], url_path='get_skills')
    def get_skills(self, request, pk=None):
        person = self.get_object()
        person_skills = BimaHrPersonSkill.objects.filter(person=person)
        serializer = BimaHrPersonSkillSerializer(person_skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'], url_path='get_experiences')
    def get_experiences(self, request, pk=None):
        person = self.get_object()
        person_experiences = BimaHrPersonExperience.objects.filter(person=person)
        serializer = BimaHrPersonExperienceSerializer(person_experiences, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        obj = BimaHrCandidat.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj


















>>>>>>> origin/ma-branch
