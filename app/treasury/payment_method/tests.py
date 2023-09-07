from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory
from .factories import BimaTreasuryPaymentMethodFactory
from .models import BimaTreasuryPaymentMethod


class BimaTreasuryPaymentMethodTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()

        self.payment_method_data = {
            'name': 'Test_payment_method',
            'active': True,
            'note': 'note payment_method',
            'code': '124578',
            'is_system': True,
            'income_outcome': 'INCOME',
            'cash_bank': 'BANK',

        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='treasury.payment_method.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.payment_method.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.payment_method.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.payment_method.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_payment_method(self):
        url = reverse('treasury:bimatreasurypaymentmethod-list')
        response = self.client.post(url, self.payment_method_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryPaymentMethod.objects.count(), 1)

    def test_get_payment_methods(self):
        BimaTreasuryPaymentMethodFactory.create_batch(5)
        url = reverse('treasury:bimatreasurypaymentmethod-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_payment_method(self):
        payment_method = BimaTreasuryPaymentMethodFactory()
        url = reverse('treasury:bimatreasurypaymentmethod-detail', kwargs={'pk': str(payment_method.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaTreasuryPaymentMethod.objects.get(pk=payment_method.pk).name, 'Updated Name')

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('treasury:bimatreasurypaymentmethod-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('treasury:bimatreasurypaymentmethod-list')
        response = self.client.post(url, self.payment_method_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        payment_method = BimaTreasuryPaymentMethodFactory()
        url = reverse('treasury:bimatreasurypaymentmethod-detail', kwargs={'pk': str(payment_method.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        payment_method = BimaTreasuryPaymentMethodFactory()
        url = reverse('treasury:bimatreasurypaymentmethod-detail', kwargs={'pk': str(payment_method.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            ('treasury.payment_method.can_create', 'Can create payment method'),
            ('treasury.payment_method.can_update', 'Can update payment method'),
            ('treasury.payment_method.can_delete', 'Can delete payment method'),
            ('treasury.payment_method.can_read', 'Can read payment method'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaTreasuryPaymentMethod)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
