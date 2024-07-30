
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


















