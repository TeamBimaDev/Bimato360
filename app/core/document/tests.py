from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import BimaCoreDocument
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory
from erp.partner.factories import BimaErpPartnerFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from erp.partner.models import BimaErpPartner
from company.factories import BimaCompanyFactory
from company.models import BimaCompany

from hr.employee.factories import BimaHrEmployeeFactory
from hr.employee.models import BimaHrEmployee
from hr.candidat.models import BimaHrCandidat
from hr.candidat.factories import BimaHrCandidatFactory
from hr.activity.factories import BimaHrActivityFactory
from hr.activity.models import BimaHrActivity


class BimaCoreDocumentTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        permission = Permission.objects.get(codename='core.document.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.document.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.document.can_delete')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.document.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='company.company.can_add_document')
        self.user.user_permissions.add(permission)
        self.file_content = "file_content".encode()

        # Give permissions to the user.
        self.client.force_authenticate(self.user)
        self.document_data = {
            "document_name": "new_document",
            "description": "This is an example description.",
            "file_name": "N0044410.jpg",
            "file_content_type": "application/octet-stream",
            "file_extension": ".txt",
            "date_file": "2023-05-15T12:30:00Z",
            "file_path": SimpleUploadedFile("N0044410.jpg", self.file_content, content_type="N0044410/jpg"),
            "file_type": "PARTNER_PICTURE",
            "is_favorite": True,
        }

    def test_create_document_with_partner(self):
        self.partner = BimaErpPartnerFactory()
        url = reverse('erp:bimaerppartner-list') + f'{self.partner.public_id}/documents/'
        self.document_data['parent_type'] = ContentType.objects.get_for_model(self.partner).id
        self.document_data['parent_id'] = self.partner.id
        response = self.client.post(url, self.document_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreDocument.objects.count(), 1)

    def test_add_document_for_partner(self):
        BimaErpPartnerFactory.create()
        self.partner = BimaErpPartner.objects.first()
        public_id = self.partner.public_id
        url = reverse('erp:bimaerppartner-list') + f'{public_id}/documents/'
        self.document_data['parent_type'] = ContentType.objects.get_for_model(self.partner).id
        self.document_data['parent_id'] = self.partner.id
        response = self.client.post(url, self.document_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreDocument.objects.count(), 1)
    def test_add_document_for_employee(self):
        BimaHrEmployeeFactory.create()
        self.employee = BimaHrEmployee.objects.first()
        public_id = self.employee.public_id
        url = reverse('hr:bimahremployee-list') + f'{public_id}/documents/'
        self.document_data['parent_type'] = ContentType.objects.get_for_model(self.employee).id
        self.document_data['parent_id'] = self.employee.id
        response = self.client.post(url, self.document_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreDocument.objects.count(), 1)

    def test_add_document_for_candidat(self):
        BimaHrCandidatFactory.create()
        self.candidat = BimaHrCandidat.objects.first()
        public_id = self.candidat.public_id
        url = reverse('hr:bimahrcandidat-list') + f'{public_id}/documents/'
        self.document_data['parent_type'] = ContentType.objects.get_for_model(self.candidat).id
        print(self.document_data['parent_type'])
        self.document_data['parent_id'] = self.candidat.id
        response = self.client.post(url, self.document_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreDocument.objects.count(), 1)

    def test_add_document_for_activity(self):
        BimaHrActivityFactory.create()
        self.activity = BimaHrActivity.objects.first()
        public_id = self.activity.public_id
        url = reverse('hr:bimahractivity-list') + f'{public_id}/documents/'
        self.document_data['parent_type'] = ContentType.objects.get_for_model(self.activity).id
        self.document_data['parent_id'] = self.activity.id
        response = self.client.post(url, self.document_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreDocument.objects.count(), 1)
        
    def test_update_document(self):
        self.test_create_document_with_partner()
        document = BimaCoreDocument.objects.first()
        document_data = {
            'document_name': 'update document name'
        }
        url = reverse('core:bimacoredocument-detail', kwargs={'pk': str(document.public_id)})
        response = self.client.patch(url, document_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaCoreDocument.objects.get(pk=document.pk).document_name, 'update document name')

    def test_add_document_for_company(self):
        BimaCompanyFactory.create()
        self.company = BimaCompany.objects.first()
        public_id = self.company.public_id
        url = reverse('bimacompany-list') + f'{public_id}/documents/'
        self.document_data['parent_type'] = ContentType.objects.get_for_model(self.company).id
        self.document_data['parent_id'] = self.company.id
        response = self.client.post(url, self.document_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreDocument.objects.count(), 1)

    def test_delete_document(self):
        self.test_create_document_with_partner()
        document = BimaCoreDocument.objects.first()
        url = reverse('core:bimacoredocument-detail', kwargs={'pk': str(document.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def create_permissions(self):
        permission_list = [
            ('core.document.can_create', 'Can create document'),
            ('core.document.can_update', 'Can update document'),
            ('core.document.can_delete', 'Can delete document'),
            ('core.document.can_read', 'Can read document'),
            ('company.company.can_add_document', 'Can add document'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaCoreDocument)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
