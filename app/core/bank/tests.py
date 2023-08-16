from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory

from .factories import BimaCoreBankFactory
from .models import BimaCoreBank


class BimaCoreBankTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()

        self.bank_data = {
            'name': 'Test Bank',
            'email': 'test@test.com',
            'active': True,
            'bic': 'TESTBIC'
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='core.bank.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.bank.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.bank.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.bank.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_bank(self):
        url = reverse('core:bimacorebank-list')
        response = self.client.post(url, self.bank_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreBank.objects.count(), 1)

    def test_get_banks(self):
        BimaCoreBankFactory.create_batch(5)
        url = reverse('core:bimacorebank-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_bank(self):
        bank = BimaCoreBankFactory()
        url = reverse('core:bimacorebank-detail', kwargs={'pk': str(bank.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaCoreBank.objects.get(pk=bank.pk).name, 'Updated Name')

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('core:bimacorebank-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('core:bimacorebank-list')
        response = self.client.post(url, self.bank_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        bank = BimaCoreBankFactory()
        url = reverse('core:bimacorebank-detail', kwargs={'pk': str(bank.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        bank = BimaCoreBankFactory()
        url = reverse('core:bimacorebank-detail', kwargs={'pk': str(bank.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            ('core.bank.can_create', 'Can create bank'),
            ('core.bank.can_update', 'Can update bank'),
            ('core.bank.can_delete', 'Can delete bank'),
            ('core.bank.can_read', 'Can read bank'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaCoreBank)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
