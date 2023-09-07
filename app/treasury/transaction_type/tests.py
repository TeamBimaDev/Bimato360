from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory
from .factories import BimaTreasuryTransactionTypeFactory
from .models import BimaTreasuryTransactionType


class BimaTreasuryTransactionTypeTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()

        self.transaction_type_data = {
            'name': 'Test_transaction_type',
            'active': True,
            'note': 'note transaction_method',
            'code': '124578',
            'is_system': True,
            'income_outcome': 'INCOME',
            'cash_bank': 'BANK',

        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='treasury.transaction_type.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.transaction_type.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.transaction_type.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.transaction_type.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_transaction_type(self):
        url = reverse('treasury:bimatreasurytransactiontype-list')
        response = self.client.post(url, self.transaction_type_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryTransactionType.objects.count(), 1)

    def test_get_transaction_types(self):
        BimaTreasuryTransactionTypeFactory.create_batch(5)
        url = reverse('treasury:bimatreasurytransactiontype-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_transaction_type(self):
        transaction_type = BimaTreasuryTransactionTypeFactory()
        url = reverse('treasury:bimatreasurytransactiontype-detail', kwargs={'pk': str(transaction_type.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaTreasuryTransactionType.objects.get(pk=transaction_type.pk).name, 'Updated Name')

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('treasury:bimatreasurytransactiontype-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('treasury:bimatreasurytransactiontype-list')
        response = self.client.post(url, self.transaction_type_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        transaction_type = BimaTreasuryTransactionTypeFactory()
        url = reverse('treasury:bimatreasurytransactiontype-detail', kwargs={'pk': str(transaction_type.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        transaction_type = BimaTreasuryTransactionTypeFactory()
        url = reverse('treasury:bimatreasurytransactiontype-detail', kwargs={'pk': str(transaction_type.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            ('treasury.transaction_type.can_create', 'Can create transaction type'),
            ('treasury.transaction_type.can_update', 'Can update transaction type'),
            ('treasury.transaction_type.can_delete', 'Can delete transaction type'),
            ('treasury.transaction_type.can_read', 'Can read transaction type'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaTreasuryTransactionType)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
