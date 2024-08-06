<<<<<<< HEAD
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .factories import BimaErpPartnerFactory
from .models import BimaErpPartner
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory


class BimaErpPartnerTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.partner_data = {
            "is_supplier": True,
            "is_customer": False,
            "partner_type": "INDIVIDUAL",
            "company_type": "GENERAL_PARTNERSHIP",
            "first_name": "John",
            "last_name": "Doe",
            "gender": "MALE",
            "social_security_number": "123456789",
            "id_number": "ABC123",
            "email": "john.doe@example.com",
            "phone": "1234567890",
            "fax": "0987654321",
            "company_name": "Example Company",
            "company_activity": "Example Activity",
            "vat_id_number": "VAT123",
            "status": "ACTIVE",
            "note": "Example note",
            "company_date_creation": "2022-01-01T00:00:00Z",
            "company_siren": "123456789",
            "company_siret": "987654321",
            "company_date_registration": "2022-01-01T00:00:00Z",
            "rcs_number": "RCS123",
            "company_date_struck_off": "2022-01-01T00:00:00Z",
            "company_ape_text": "Example APE Text",
            "company_ape_code": "APE123",
            "company_capital": "10000 USD",
            "credit": 1212.21,
            "balance": 2323.12
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='erp.partner.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='erp.partner.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='erp.partner.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='erp.partner.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_partner(self):
        url = reverse('erp:bimaerppartner-list')
        response = self.client.post(url, self.partner_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaErpPartner.objects.count(), 1)

    def test_get_partners(self):
        BimaErpPartnerFactory.create_batch(5)
        url = reverse('erp:bimaerppartner-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_partner(self):
        partner = BimaErpPartnerFactory()
        url = reverse('erp:bimaerppartner-detail', kwargs={'pk': str(partner.public_id)})
        data = {'first_name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaErpPartner.objects.get(pk=partner.pk).first_name, 'Updated Name')

   # def test_delete_partner(self):
    #    partner = BimaErpPartnerFactory()
     #   url = reverse('erp:bimaerppartner-detail', kwargs={'pk': str(partner.public_id)})
      #  response = self.client.delete(url, format='json')
       # self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('erp:bimaerppartner-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('erp:bimaerppartner-list')
        response = self.client.post(url, self.partner_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        partner = BimaErpPartnerFactory()
        url = reverse('erp:bimaerppartner-detail', kwargs={'pk': str(partner.public_id)})
        data = {'first_name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        partner = BimaErpPartnerFactory()
        url = reverse('erp:bimaerppartner-detail', kwargs={'pk': str(partner.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('erp.partner.can_create', 'Can create partner'),
            ('erp.partner.can_update', 'Can update partner'),
            ('erp.partner.can_delete', 'Can delete partner'),
            ('erp.partner.can_read', 'Can read partner'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaErpPartner)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
=======
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .factories import BimaErpPartnerFactory
from .models import BimaErpPartner
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory


class BimaErpPartnerTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.partner_data = {
            "is_supplier": True,
            "is_customer": False,
            "partner_type": "INDIVIDUAL",
            "company_type": "GENERAL_PARTNERSHIP",
            "first_name": "John",
            "last_name": "Doe",
            "gender": "MALE",
            "social_security_number": "123456789",
            "id_number": "ABC123",
            "email": "john.doe@example.com",
            "phone": "1234567890",
            "fax": "0987654321",
            "company_name": "Example Company",
            "company_activity": "Example Activity",
            "vat_id_number": "VAT123",
            "status": "ACTIVE",
            "note": "Example note",
            "company_date_creation": "2022-01-01T00:00:00Z",
            "company_siren": "123456789",
            "company_siret": "987654321",
            "company_date_registration": "2022-01-01T00:00:00Z",
            "rcs_number": "RCS123",
            "company_date_struck_off": "2022-01-01T00:00:00Z",
            "company_ape_text": "Example APE Text",
            "company_ape_code": "APE123",
            "company_capital": "10000 USD",
            "credit": 1212.21,
            "balance": 2323.12
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='erp.partner.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='erp.partner.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='erp.partner.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='erp.partner.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_partner(self):
        url = reverse('erp:bimaerppartner-list')
        response = self.client.post(url, self.partner_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaErpPartner.objects.count(), 1)

    def test_get_partners(self):
        BimaErpPartnerFactory.create_batch(5)
        url = reverse('erp:bimaerppartner-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_partner(self):
        partner = BimaErpPartnerFactory()
        url = reverse('erp:bimaerppartner-detail', kwargs={'pk': str(partner.public_id)})
        data = {'first_name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaErpPartner.objects.get(pk=partner.pk).first_name, 'Updated Name')

   # def test_delete_partner(self):
    #    partner = BimaErpPartnerFactory()
     #   url = reverse('erp:bimaerppartner-detail', kwargs={'pk': str(partner.public_id)})
      #  response = self.client.delete(url, format='json')
       # self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('erp:bimaerppartner-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('erp:bimaerppartner-list')
        response = self.client.post(url, self.partner_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        partner = BimaErpPartnerFactory()
        url = reverse('erp:bimaerppartner-detail', kwargs={'pk': str(partner.public_id)})
        data = {'first_name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        partner = BimaErpPartnerFactory()
        url = reverse('erp:bimaerppartner-detail', kwargs={'pk': str(partner.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('erp.partner.can_create', 'Can create partner'),
            ('erp.partner.can_update', 'Can update partner'),
            ('erp.partner.can_delete', 'Can delete partner'),
            ('erp.partner.can_read', 'Can read partner'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaErpPartner)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
>>>>>>> origin/ma-branch
            )