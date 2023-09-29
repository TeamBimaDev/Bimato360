import logging

from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet
from core.address.models import get_addresses_for_parent, create_single_address, BimaCoreAddress
from core.address.serializers import BimaCoreAddressSerializer
from core.contact.models import get_contacts_for_parent_entity, create_single_contact, BimaCoreContact
from core.contact.serializers import BimaCoreContactSerializer
from core.document.models import BimaCoreDocument, get_documents_for_parent_entity
from core.document.serializers import BimaCoreDocumentSerializer
from django.shortcuts import get_object_or_404
from hr.models import BimaHrPersonSkill, BimaHrPersonExperience
from hr.serializers import BimaHrPersonSkillSerializer, BimaHrPersonExperienceSerializer
from hr.service import delete_person_experience, delete_person_skill, add_or_update_person_skill, \
    add_or_update_person_experience
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from treasury.bank_account.models import BimaTreasuryBankAccount
from treasury.bank_account.serializers import BimaTreasuryBankAccountSerializer
from treasury.bank_account.service import BimaTreasuryBankAccountService

from .filters import BimaHrEmployeeFilter
from .models import BimaHrEmployee
from .serializers import BimaHrEmployeeSerializer

logger = logging.getLogger(__name__)


class BimaHrEmployeeViewSet(AbstractViewSet):
    queryset = BimaHrEmployee.objects.all()
    serializer_class = BimaHrEmployeeSerializer
    ordering = ["-first_name"]
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    filterset_class = BimaHrEmployeeFilter
    action_permissions = {
        'list': ['employee.can_read'],
        'create': ['employee.can_create'],
        'retrieve': ['employee.can_read'],
        'update': ['employee.can_update'],
        'partial_update': ['employee.can_update'],
        'destroy': ['employee.can_delete'],
        'documents': ['employee.can_add_document'],
        'bank_accounts': ['employee.can_add_bank_account'],
        'contacts': ['employee.can_add_contact'],
        'addresses': ['employee.can_add_address'],
        'delete_skill': ['employee.can_manage_skill'],
        'add_update_skill': ['employee.can_manage_skill'],
        'get_person_skills': ['employee.can_manage_skill'],
        'delete_experience': ['employee.can_manage_experience'],
        'get_skills': ['employee.can_manage_skill'],
        'get_experiences': ['employee.can_manage_experience'],
    }

    def list_documents(self, request, *args, **kwargs):
        employee = BimaHrEmployee.objects.get_object_by_public_id(self.kwargs['public_id'])
        documents = get_documents_for_parent_entity(employee)
        serialized_document = BimaCoreDocumentSerializer(documents, many=True)
        return Response(serialized_document.data)

    def create_document(self, request, *args, **kwargs):
        employee = BimaHrEmployee.objects.get_object_by_public_id(self.kwargs['public_id'])
        document_data = request.data
        document_data['file_path'] = request.FILES['file_path']
        result = BimaCoreDocument.create_document_for_parent(employee, document_data)
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
        employee = BimaHrEmployee.objects.get_object_by_public_id(self.kwargs['public_id'])
        document = get_object_or_404(BimaCoreDocument,
                                     public_id=self.kwargs['document_public_id'],
                                     parent_id=employee.id)
        serialized_document = BimaCoreDocumentSerializer(document)
        return Response(serialized_document.data)

    def list_bank_account(self, request, *args, **kwargs):
        employee = BimaHrEmployee.objects.get_object_by_public_id(self.kwargs['public_id'])
        bank_accounts = BimaTreasuryBankAccountService.get_bank_accounts_for_parent_entity(employee)
        serialized_bank_account = BimaTreasuryBankAccountSerializer(bank_accounts, many=True)
        return Response(serialized_bank_account.data)

    def create_bank_account(self, request, *args, **kwargs):
        employee = BimaHrEmployee.objects.get_object_by_public_id(self.kwargs['public_id'])
        bank_account_data = request.data
        result = BimaTreasuryBankAccountService.create_bank_account(employee, bank_account_data)
        if isinstance(result, BimaTreasuryBankAccount):
            serialized_bank_account = BimaTreasuryBankAccountSerializer(result)
            return Response(serialized_bank_account.data, status=status.HTTP_201_CREATED)
        else:
            return Response(result, status=result.get("status", status.HTTP_500_INTERNAL_SERVER_ERROR))

    def get_bank_account(self, request, *args, **kwargs):
        employee = BimaHrEmployee.objects.get_object_by_public_id(self.kwargs['public_id'])
        bank_account = BimaTreasuryBankAccountService.get_bank_account_by_public_id_and_parent(
            public_id=self.kwargs['bank_account_public_id'],
            parent_id=employee.id)
        if not bank_account:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        serialized_bank_account = BimaTreasuryBankAccountSerializer(bank_account)
        return Response(serialized_bank_account.data)

    def list_addresses(self, request, *args, **kwargs):
        employee = BimaHrEmployee.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        addresses = get_addresses_for_parent(employee)
        serialized_addresses = BimaCoreAddressSerializer(addresses, many=True)
        return Response(serialized_addresses.data)

    def create_address(self, request, *args, **kwargs):
        employee = BimaHrEmployee.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        response = create_single_address(request.data, employee)
        if "error" in response:
            return Response({"detail": response["error"]}, status=response["status"])
        return Response(response["data"], status=response["status"])

    def get_address(self, request, *args, **kwargs):
        employee = BimaHrEmployee.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        address = get_object_or_404(
            BimaCoreAddress,
            public_id=self.kwargs["address_public_id"],
            parent_id=employee.id,
        )
        serialized_address = BimaCoreAddressSerializer(address)
        return Response(serialized_address.data)

    def list_contacts(self, request, *args, **kwargs):
        employee = BimaHrEmployee.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        contacts = get_contacts_for_parent_entity(employee)
        serialized_contact = BimaCoreContactSerializer(contacts, many=True)
        return Response(serialized_contact.data)

    def create_contact(self, request, *args, **kwargs):
        employee = BimaHrEmployee.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        response = create_single_contact(request.data, employee)
        if "error" in response:
            return Response({"detail": response["error"]}, status=response["status"])
        return Response(response["data"], status=response["status"])

    def get_contact(self, request, *args, **kwargs):
        employee = BimaHrEmployee.objects.get_object_by_public_id(
            self.kwargs["public_id"]
        )
        contact = get_object_or_404(
            BimaCoreContact,
            public_id=self.kwargs["contact_public_id"],
            parent_id=employee.id,
        )
        serialized_contact = BimaCoreContactSerializer(contact)
        return Response(serialized_contact.data)

    @action(detail=True, methods=['POST'], url_path='add_update_skill')
    def add_update_skill(self, request, pk=None):
        employee = self.get_object()
        skill_public_id = request.data.get('skill_public_id')
        level = request.data.get('level')

        try:
            person_skill, created = add_or_update_person_skill(employee, skill_public_id, level)
            if created:
                return Response({'status': 'Skill added'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'status': 'Skill updated'}, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response(e.detail, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['DELETE'], url_path='delete_skill')
    def delete_skill(self, request, pk=None):
        employee = self.get_object()
        skill_public_id = request.data.get('skill_public_id')

        try:
            delete_person_skill(employee, skill_public_id)
            return Response({'status': 'Skill deleted'}, status=status.HTTP_204_NO_CONTENT)
        except NotFound as e:
            return Response(e.detail, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST', 'PUT'], url_path='add_update_experience')
    def add_update_experience(self, request, pk=None):
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
        obj = BimaHrEmployee.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
