from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .factories import BimaCoreCurrencyFactory
from .models import BimaCoreCurrency
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory


class BimaCoreCurrencyTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()

        self.currency_data = {
              "name": "US Dollar",
              "symbol": "$",
              "decimal_places": 2,
              "active": True,
              "currency_unit_label": "USD",
              "currency_subunit_label": "Cent"
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='core.currency.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.currency.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.currency.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.currency.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_currency(self):
        url = reverse('core:bimacorecurrency-list')
        response = self.client.post(url, self.currency_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreCurrency.objects.count(), 1)

    def test_get_currencys(self):
        BimaCoreCurrencyFactory.create_batch(5)
        url = reverse('core:bimacorecurrency-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_currency(self):
        currency = BimaCoreCurrencyFactory()
        url = reverse('core:bimacorecurrency-detail', kwargs={'pk': str(currency.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaCoreCurrency.objects.get(pk=currency.pk).name, 'Updated Name')

    def test_delete_currency(self):
        currency = BimaCoreCurrencyFactory()
        url = reverse('core:bimacorecurrency-detail', kwargs={'pk': str(currency.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('core:bimacorecurrency-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('core:bimacorecurrency-list')
        response = self.client.post(url, self.currency_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        currency = BimaCoreCurrencyFactory()
        url = reverse('core:bimacorecurrency-detail', kwargs={'pk': str(currency.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        currency = BimaCoreCurrencyFactory()
        url = reverse('core:bimacorecurrency-detail', kwargs={'pk': str(currency.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('core.currency.can_create', 'Can create currency'),
            ('core.currency.can_update', 'Can update currency'),
            ('core.currency.can_delete', 'Can delete currency'),
            ('core.currency.can_read', 'Can read currency'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaCoreCurrency)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )