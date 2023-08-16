from core.bank.factories import BimaCoreBankFactory
from core.bank.models import BimaCoreBank
from core.country.factories import BimaCoreCountryFactory
from core.state.factories import BimaCoreStateFactory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from erp.partner.factories import BimaErpPartnerFactory
from erp.partner.models import BimaErpPartner
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory

from .models import BimaCoreAddress


class BimaCoreAddressTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.state = BimaCoreStateFactory.create()
        self.country = BimaCoreCountryFactory.create()
        permission = Permission.objects.get(codename='core.address.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.address.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.address.can_delete')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.address.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='company.company.can_add_address')
        self.user.user_permissions.add(permission)
        self.address_data = {
            'number': '123',
            'street': 'Test Street',
            'zip': '12345',
            'city': 'Test City',
            'contact_name': 'Contact name',
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

    def test_update_address(self):
        self.test_create_address_with_bank()
        address = BimaCoreAddress.objects.first()
        address_data = {
            'contact_name': 'update contact name'
        }
        url = reverse('core:bimacoreaddress-detail', kwargs={'pk': str(address.public_id)})
        response3 = self.client.patch(url, address_data, format='json')
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaCoreAddress.objects.get(pk=address.pk).contact_name, 'update contact name')

    def test_delete_address(self):
        self.test_create_address_with_bank()
        address = BimaCoreAddress.objects.first()
        url = reverse('core:bimacoreaddress-detail', kwargs={'pk': str(address.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_add_address_for_bank(self):
        BimaCoreBankFactory.create()
        self.bank = BimaCoreBank.objects.first()
        public_id = self.bank.public_id
        url2 = reverse('core:bimacorebank-list') + f'{public_id}/addresses/'
        self.address_data['parent_type'] = ContentType.objects.get_for_model(self.bank).id
        self.address_data['parent_id'] = self.bank.id
        response = self.client.post(url2, self.address_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreAddress.objects.count(), 1)

    def test_add_address_for_partner(self):
        BimaErpPartnerFactory.create()
        self.partner = BimaErpPartner.objects.first()
        public_id = self.partner.public_id
        url2 = reverse('erp:bimaerppartner-list') + f'{public_id}/addresses/'
        self.address_data['parent_type'] = ContentType.objects.get_for_model(self.partner).id
        self.address_data['parent_id'] = self.partner.id
        response = self.client.post(url2, self.address_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreAddress.objects.count(), 1)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('core:bimacoreaddress-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('core.address.can_create', 'Can create address'),
            ('core.address.can_update', 'Can update address'),
            ('core.address.can_delete', 'Can delete address'),
            ('core.address.can_read', 'Can read address'),
            ('company.company.can_add_address', 'Can add address'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaCoreAddress)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
