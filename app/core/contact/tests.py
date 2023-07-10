from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import BimaCoreContact
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory
from erp.partner.factories import BimaErpPartnerFactory
from erp.partner.models import BimaErpPartner


class BimaCoreContactTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        permission = Permission.objects.get(codename='erp.partner.can_create')
        self.user.user_permissions.add(permission)
        self.contact_data = {
            "name": "John Doe",
            "position": "Manager",
            "department": "Sales",
            "email": "johndoe@example.com",
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


    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('erp.partner.can_create', 'Can create partner'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaErpPartner)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )