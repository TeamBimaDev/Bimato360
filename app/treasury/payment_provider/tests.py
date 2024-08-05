<<<<<<< HEAD
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory
from .factories import BimaTreasuryPaymentProviderFactory
from .models import BimaTreasuryPaymentProvider


class BimaTreasuryPaymentProviderTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()

        self.payment_provider_data = {
                "name": "Fournisseur1",
                "active": True,
                "credentials": {},
                "supports_tokenization": True,
                "supports_manual_capture": False,
                "supports_refunds": True

        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='treasury.payment_provider.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.payment_provider.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.payment_provider.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.payment_provider.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_payment_provider(self):
        url = reverse('treasury:bimatreasurypaymentprovider-list')
        response = self.client.post(url, self.payment_provider_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryPaymentProvider.objects.count(), 1)

    def test_get_payment_providers(self):
        BimaTreasuryPaymentProviderFactory.create_batch(5)
        url = reverse('treasury:bimatreasurypaymentprovider-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_payment_provider(self):
        payment_provider = BimaTreasuryPaymentProviderFactory()
        url = reverse('treasury:bimatreasurypaymentprovider-detail', kwargs={'pk': str(payment_provider.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaTreasuryPaymentProvider.objects.get(pk=payment_provider.pk).name, 'Updated Name')

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('treasury:bimatreasurypaymentprovider-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('treasury:bimatreasurypaymentprovider-list')
        response = self.client.post(url, self.payment_provider_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        payment_provider = BimaTreasuryPaymentProviderFactory()
        url = reverse('treasury:bimatreasurypaymentprovider-detail', kwargs={'pk': str(payment_provider.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        payment_provider = BimaTreasuryPaymentProviderFactory()
        url = reverse('treasury:bimatreasurypaymentprovider-detail', kwargs={'pk': str(payment_provider.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            ('treasury.payment_provider.can_create', 'Can create payment provider'),
            ('treasury.payment_provider.can_update', 'Can update payment provider'),
            ('treasury.payment_provider.can_delete', 'Can delete payment provider'),
            ('treasury.payment_provider.can_read', 'Can read payment provider'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaTreasuryPaymentProvider)
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
from .factories import BimaTreasuryPaymentProviderFactory
from .models import BimaTreasuryPaymentProvider


class BimaTreasuryPaymentProviderTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()

        self.payment_provider_data = {
                "name": "Fournisseur1",
                "active": True,
                "credentials": {},
                "supports_tokenization": True,
                "supports_manual_capture": False,
                "supports_refunds": True

        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='treasury.payment_provider.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.payment_provider.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.payment_provider.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.payment_provider.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_payment_provider(self):
        url = reverse('treasury:bimatreasurypaymentprovider-list')
        response = self.client.post(url, self.payment_provider_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryPaymentProvider.objects.count(), 1)

    def test_get_payment_providers(self):
        BimaTreasuryPaymentProviderFactory.create_batch(5)
        url = reverse('treasury:bimatreasurypaymentprovider-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_payment_provider(self):
        payment_provider = BimaTreasuryPaymentProviderFactory()
        url = reverse('treasury:bimatreasurypaymentprovider-detail', kwargs={'pk': str(payment_provider.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaTreasuryPaymentProvider.objects.get(pk=payment_provider.pk).name, 'Updated Name')

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('treasury:bimatreasurypaymentprovider-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('treasury:bimatreasurypaymentprovider-list')
        response = self.client.post(url, self.payment_provider_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        payment_provider = BimaTreasuryPaymentProviderFactory()
        url = reverse('treasury:bimatreasurypaymentprovider-detail', kwargs={'pk': str(payment_provider.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        payment_provider = BimaTreasuryPaymentProviderFactory()
        url = reverse('treasury:bimatreasurypaymentprovider-detail', kwargs={'pk': str(payment_provider.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            ('treasury.payment_provider.can_create', 'Can create payment provider'),
            ('treasury.payment_provider.can_update', 'Can update payment provider'),
            ('treasury.payment_provider.can_delete', 'Can delete payment provider'),
            ('treasury.payment_provider.can_read', 'Can read payment provider'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaTreasuryPaymentProvider)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
>>>>>>> origin/ma-branch
