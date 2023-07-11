from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import BimaCoreDocument
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory
from erp.partner.factories import BimaErpPartnerFactory
from erp.partner.models import BimaErpPartner


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
        self.document_data = {
                  "document_name": "new_document",
                  "description": "This is an example description.",
                  "file_name": "N0044410.txt",
                  "file_content_type": "application/octet-stream",
                  "file_extension": ".txt",
                  "date_file": "2023-05-15T12:30:00Z",
                  "file_path": "C:/Users/Dell/Desktop/text/N0044410.txt",
                  "file_type": "PARTNER_PICTURE",
                  "is_favorite": True
                }
        # Give permissions to the user.
        self.client.force_authenticate(self.user)
    def test_create_document_with_partner(self):
        self.partner = BimaErpPartnerFactory()
        public_id = self.partner.public_id
        url = reverse('erp:bimaerppartner-list') + f'{public_id}/documents/'
        self.document_data['parent_type'] = ContentType.objects.get_for_model(self.partner).id
        self.document_data['parent_id'] = self.partner.id
        response = self.client.post(url, self.document_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreDocument.objects.count(), 1)
    def test_add_document_for_partner(self):
        BimaErpPartnerFactory.create()
        self.partner = BimaErpPartner.objects.first()
        public_id = self.partner.public_id
        url2 = reverse('erp:bimaerppartner-list') + f'{public_id}/documents/'
        self.document_data['parent_type'] = ContentType.objects.get_for_model(self.partner).id
        self.document_data['parent_id'] = self.partner.id
        response = self.client.post(url2, self.document_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreDocument.objects.count(), 1)
    def test_update_document(self):
        self.test_create_document_with_partner()
        document = BimaCoreDocument.objects.first()
        document_data = {
            'document_name': 'update document name'
        }
        url = reverse('core:bimacoredocument-detail', kwargs={'pk': str(document.public_id)})
        response3 = self.client.patch(url, document_data, format='json')
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaCoreDocument.objects.get(pk=document.pk).document_name, 'update document name')
    def test_delete_document(self):
        self.test_create_document_with_partner()
        document = BimaCoreDocument.objects.first()
        url = reverse('core:bimacoredocument-detail', kwargs={'pk': str(document.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
   # def test_unauthorized_create_contact_with_partner(self):
    #    self.client.logout()
    #    user_without_permission = UserFactory()
    #    self.client.force_authenticate(user_without_permission)
    #    BimaErpPartnerFactory.create()
    #    self.partner = BimaErpPartner.objects.first()
    #    public_id = self.partner.public_id
    #    url2 = reverse('erp:bimaerppartner-list') + f'{public_id}/contacts/'
    #    self.contact_data['parent_type'] = ContentType.objects.get_for_model(self.partner).id
    #    self.contact_data['parent_id'] = self.partner.id
    #    response = self.client.post(url2, self.contact_data, format='json')
    #    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #def test_unauthorized_add_contact_for_partner(self):
    #    self.client.logout()
    #    user_without_permission = UserFactory()
    #    self.client.force_authenticate(user_without_permission)
    #    self.partner = BimaErpPartnerFactory()
    #    public_id = self.partner.public_id
    #    url = reverse('erp:bimaerppartner-list') + f'{public_id}/contacts/'
    #    self.contact_data['parent_type'] = ContentType.objects.get_for_model(self.partner).id
    #    self.contact_data['parent_id'] = self.partner.id
    #    response = self.client.post(url, self.contact_data, format='json')
    #    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('core:bimacoredocument-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        self.test_create_document_with_partner()
        document = BimaCoreDocument.objects.first()
        url = reverse('core:bimacoredocument-detail', kwargs={'pk': str(document.public_id)})
        data = {'document_name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        self.test_create_document_with_partner()
        document = BimaCoreDocument.objects.first()
        url = reverse('core:bimacoredocument-detail', kwargs={'pk': str(document.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('core.document.can_create', 'Can create document'),
            ('core.document.can_update', 'Can update document'),
            ('core.document.can_delete', 'Can delete document'),
            ('core.document.can_read', 'Can read document'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaCoreDocument)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )