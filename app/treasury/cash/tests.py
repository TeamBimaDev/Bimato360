from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory
from .factories import BimaTreasuryCashFactory
from .models import BimaTreasuryCash
from company.factories import BimaCompanyFactory


class BimaTreasuryCashTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.company = BimaCompanyFactory.create()

        self.cash_data = {
            'name': 'Test Cash',
            'active': True,
            'company_public_id': str(self.company.public_id),
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='treasury.cash.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.cash.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.cash.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.cash.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_cash(self):
        url = reverse('treasury:bimatreasurycash-list')
        response = self.client.post(url, self.cash_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryCash.objects.count(), 1)

    def test_get_cashs(self):
        BimaTreasuryCashFactory.create_batch(5)
        url = reverse('treasury:bimatreasurycash-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_cash(self):
        cash = BimaTreasuryCashFactory()
        url = reverse('treasury:bimatreasurycash-detail', kwargs={'pk': str(cash.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaTreasuryCash.objects.get(pk=cash.pk).name, 'Updated Name')

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('treasury:bimatreasurycash-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('treasury:bimatreasurycash-list')
        response = self.client.post(url, self.cash_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        cash = BimaTreasuryCashFactory()
        url = reverse('treasury:bimatreasurycash-detail', kwargs={'pk': str(cash.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        cash = BimaTreasuryCashFactory()
        url = reverse('treasury:bimatreasurycash-detail', kwargs={'pk': str(cash.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            ('treasury.cash.can_create', 'Can create cash'),
            ('treasury.cash.can_update', 'Can update cash'),
            ('treasury.cash.can_delete', 'Can delete cash'),
            ('treasury.cash.can_read', 'Can read cash'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaTreasuryCash)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
