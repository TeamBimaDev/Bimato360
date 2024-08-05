<<<<<<< HEAD
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory
from .factories import BimaTreasuryRefundFactory
from .models import BimaTreasuryRefund
from treasury.transaction.factories import BimaTreasuryTransactionFactory


class BimaTreasuryRefundTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.transaction = BimaTreasuryTransactionFactory.create()

        self.refund_data = {
            'transaction_public_id': str(self.transaction.public_id),
            "amount": "50.678",
            "reason": "Refund Reason",
            "date": "2023-09-22"
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='treasury.refund.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.refund.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.refund.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.refund.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_refund(self):
        url = reverse('treasury:bimatreasuryrefund-list')
        response = self.client.post(url, self.refund_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryRefund.objects.count(), 1)

    def test_get_refunds(self):
        BimaTreasuryRefundFactory.create_batch(5)
        url = reverse('treasury:bimatreasuryrefund-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_refund(self):
        refund = BimaTreasuryRefundFactory()
        url = reverse('treasury:bimatreasuryrefund-detail', kwargs={'pk': str(refund.public_id)})
        data = {'reason': 'Updated reason'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaTreasuryRefund.objects.get(pk=refund.pk).name, 'Updated reason')

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('treasury:bimatreasuryrefund-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('treasury:bimatreasuryrefund-list')
        response = self.client.post(url, self.refund_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        refund = BimaTreasuryRefundFactory()
        url = reverse('treasury:bimatreasuryrefund-detail', kwargs={'pk': str(refund.public_id)})
        data = {'reason': 'Updated reason'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        refund = BimaTreasuryRefundFactory()
        url = reverse('treasury:bimatreasuryrefund-detail', kwargs={'pk': str(refund.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            ('treasury.refund.can_create', 'Can create refund'),
            ('treasury.refund.can_update', 'Can update refund'),
            ('treasury.refund.can_delete', 'Can delete refund'),
            ('treasury.refund.can_read', 'Can read refund'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaTreasuryRefund)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
=======
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory
from .factories import BimaTreasuryRefundFactory
from .models import BimaTreasuryRefund
from treasury.transaction.factories import BimaTreasuryTransactionFactory


class BimaTreasuryRefundTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.transaction = BimaTreasuryTransactionFactory.create()

        self.refund_data = {
            'transaction_public_id': str(self.transaction.public_id),
            "amount": "50.678",
            "reason": "Refund Reason",
            "date": "2023-09-22"
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='treasury.refund.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.refund.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.refund.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.refund.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_refund(self):
        url = reverse('treasury:bimatreasuryrefund-list')
        response = self.client.post(url, self.refund_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryRefund.objects.count(), 1)

    def test_get_refunds(self):
        BimaTreasuryRefundFactory.create_batch(5)
        url = reverse('treasury:bimatreasuryrefund-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_refund(self):
        refund = BimaTreasuryRefundFactory()
        url = reverse('treasury:bimatreasuryrefund-detail', kwargs={'pk': str(refund.public_id)})
        data = {'reason': 'Updated reason'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaTreasuryRefund.objects.get(pk=refund.pk).name, 'Updated reason')

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('treasury:bimatreasuryrefund-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('treasury:bimatreasuryrefund-list')
        response = self.client.post(url, self.refund_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        refund = BimaTreasuryRefundFactory()
        url = reverse('treasury:bimatreasuryrefund-detail', kwargs={'pk': str(refund.public_id)})
        data = {'reason': 'Updated reason'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        refund = BimaTreasuryRefundFactory()
        url = reverse('treasury:bimatreasuryrefund-detail', kwargs={'pk': str(refund.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            ('treasury.refund.can_create', 'Can create refund'),
            ('treasury.refund.can_update', 'Can update refund'),
            ('treasury.refund.can_delete', 'Can delete refund'),
            ('treasury.refund.can_read', 'Can read refund'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaTreasuryRefund)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
>>>>>>> origin/ma-branch
