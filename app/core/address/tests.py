from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .factories import BimaCoreAddressFactory
from .models import BimaCoreAddress
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory
from core.bank.factories import BimaCoreBankFactory
from core.country.factories import BimaCoreCountryFactory
from core.state.factories import BimaCoreStateFactory
from core.bank.models import BimaCoreBank
from erp.partner.factories import BimaErpPartnerFactory


class BimaCoreAddressTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.state = BimaCoreStateFactory.create()
        self.country = BimaCoreCountryFactory.create()
        permission = Permission.objects.get(codename='core.bank.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='erp.partner.can_create')
        self.user.user_permissions.add(permission)
        self.address_data = {
            'number': '123',
            'street': 'Test Street',
            'zip': '12345',
            'city': 'Test City',
            'contact_name': 'John Doe',
            'contact_phone': '1234567890',
            'contact_email': 'test@example.com',
            'can_send_bill': True,
            'can_deliver': False,
            'latitude': '12.345678',
            'longitude': '98.7654321',
            'note': 'Test address',
            'state_public_id': str(self.state.public_id),
            'country_public_id': str(self.country.public_id),
        }
        # Give permissions to the user.
        self.client.force_authenticate(self.user)
    def test_create_address_with_bank(self):
        self.bank = BimaCoreBankFactory()
        public_id = self.bank.public_id
        url = reverse('core:bimacorebank-list') + f'{public_id}/addresses/'
        self.address_data['parent_type'] = ContentType.objects.get_for_model(self.bank).id
        self.address_data['parent_id'] = self.bank.id
        response = self.client.post(url, self.address_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreAddress.objects.count(), 1)
    def test_create_address_with_partner(self):
        self.partner = BimaErpPartnerFactory()
        public_id = self.partner.public_id
        url = reverse('erp:bimaerppartner-list') + f'{public_id}/addresses/'
        self.address_data['parent_type'] = ContentType.objects.get_for_model(self.partner).id
        self.address_data['parent_id'] = self.partner.id
        response = self.client.post(url, self.address_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreAddress.objects.count(), 1)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('core.bank.can_create', 'Can create bank'),
            ('erp.partner.can_update', 'Can update partner'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaCoreBank)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )