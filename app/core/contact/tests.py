from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from erp.partner.factories import BimaErpPartnerFactory
from erp.partner.models import BimaErpPartner
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory

from .models import BimaCoreContact
from hr.employee.factories import BimaHrEmployeeFactory
from hr.employee.models import BimaHrEmployee


class BimaCoreContactTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        permission = Permission.objects.get(codename='erp.partner.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.contact.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.contact.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.contact.can_delete')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.contact.can_read')
        self.user.user_permissions.add(permission)
        self.contact_data = {
            "name": "MED",
            "position": "Manager",
            "department": "Sales",
            "email": "Med@example.com",
            "fax": "123456789",
            "mobile": "987654321",
            "phone": "555555555",
            "gender": "MALE"
        }
        # Give permissions to the user.
        self.client.force_authenticate(self.user)

    def test_create_contact_with_partner(self):
        self.partner = BimaErpPartnerFactory()
        public_id = self.partner.public_id
        url = reverse('erp:bimaerppartner-list') + f'{public_id}/contacts/'
        self.contact_data['parent_type'] = ContentType.objects.get_for_model(self.partner).id
        self.contact_data['parent_id'] = self.partner.id
        response = self.client.post(url, self.contact_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreContact.objects.count(), 1)

    def test_add_contact_for_partner(self):
        BimaErpPartnerFactory.create()
        self.partner = BimaErpPartner.objects.first()
        public_id = self.partner.public_id
        url2 = reverse('erp:bimaerppartner-list') + f'{public_id}/contacts/'
        self.contact_data['parent_type'] = ContentType.objects.get_for_model(self.partner).id
        self.contact_data['parent_id'] = self.partner.id
        response = self.client.post(url2, self.contact_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreContact.objects.count(), 1)
    def test_add_contact_for_employee(self):
        BimaHrEmployeeFactory.create()
        self.employee = BimaHrEmployee.objects.first()
        public_id = self.employee.public_id
        url2 = reverse('hr:bimahremployee-list') + f'{public_id}/contacts/'
        self.contact_data['parent_type'] = ContentType.objects.get_for_model(self.employee).id
        self.contact_data['parent_id'] = self.employee.id
        response = self.client.post(url2, self.contact_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreContact.objects.count(), 1)
    def test_update_contact(self):
        self.test_create_contact_with_partner()
        contact = BimaCoreContact.objects.first()
        contact_data = {
            'name': 'update contact name'
        }
        url = reverse('core:bimacorecontact-detail', kwargs={'pk': str(contact.public_id)})
        response3 = self.client.patch(url, contact_data, format='json')
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaCoreContact.objects.get(pk=contact.pk).name, 'update contact name')

    def test_delete_contact(self):
        self.test_create_contact_with_partner()
        contact = BimaCoreContact.objects.first()
        url = reverse('core:bimacorecontact-detail', kwargs={'pk': str(contact.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('core:bimacorecontact-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('erp.partner.can_create', 'Can create partner'),
            ('core.contact.can_create', 'Can create contact'),
            ('core.contact.can_update', 'Can update contact'),
            ('core.contact.can_delete', 'Can delete contact'),
            ('core.contact.can_read', 'Can read contact'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaCoreContact)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
