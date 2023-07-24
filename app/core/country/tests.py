from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .factories import BimaCoreCountryFactory
from .models import BimaCoreCountry
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory
from core.currency.factories import BimaCoreCurrencyFactory


class BimaCoreCountryTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.currency = BimaCoreCurrencyFactory.create()
        self.country = BimaCoreCountryFactory.create()
        self.country_data = {
            "name": "Test country",
            "code": "TC",
            "iso3": "iso3",
            "iso2": "iso2",
            "address_format": "Test address format",
            "capital": "capital1",
            "phone_code": 1234,
            "vat_label": "VAT",
            "zip_required": True,
            "currency_public_id": str(self.currency.public_id)
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='core.country.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.country.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.country.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.country.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_country(self):
        url = reverse('core:bimacorecountry-list')
        response = self.client.post(url, self.country_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreCountry.objects.count(), 2)

    def test_get_countries(self):
        BimaCoreCountryFactory.create_batch(5)
        url = reverse('core:bimacorecountry-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 6)
        self.assertEqual(len(response.data['results']), 6)

    def test_update_country(self):
        country = BimaCoreCountryFactory()
        url = reverse('core:bimacorecountry-detail', kwargs={'pk': str(country.public_id)})
        data = {'name': 'Updated Name',
                "currency_public_id": str(self.currency.public_id),
                }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaCoreCountry.objects.get(pk=country.pk).name, 'Updated Name')

    def test_delete_country(self):
        country = BimaCoreCountryFactory()
        url = reverse('core:bimacorecountry-detail', kwargs={'pk': str(country.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('core:bimacorecountry-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('core:bimacorecountry-list')
        response = self.client.post(url, self.country_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        country = BimaCoreCountryFactory()
        url = reverse('core:bimacorecountry-detail', kwargs={'pk': str(country.public_id)})
        data = {'name': 'Updated Name',
                "currency_public_id": str(self.currency.public_id),

                }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        country = BimaCoreCountryFactory()
        url = reverse('core:bimacorecountry-detail', kwargs={'pk': str(country.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unique_name(self):
        url = reverse('core:bimacorecountry-list')
        data = {
            "name": self.country.name,
            "code": "TC2",
            "iso3": "iso3",
            "iso2": "iso2",
            "address_format": "Test address format",
            "capital": "capital1",
            "phone_code": 1234,
            "vat_label": "VAT",
            "zip_required": True,
            "currency_public_id": str(self.currency.public_id)
        }
        response = self.client.post(url, data)
        BimaCoreCountry.objects.get(name=self.country.name)
        self.assertEqual(BimaCoreCountry.objects.count(), 1)
        self.assertEqual(response.status_code, 400)

    def test_unique_code(self):
        url = reverse('core:bimacorecountry-list')
        data = {
            "code": self.country.code,
            "name": "TC12",
            "iso3": "iso3",
            "iso2": "iso2",
            "address_format": "Test address format",
            "capital": "capital1",
            "phone_code": 1234,
            "vat_label": "VAT",
            "zip_required": True,
            "currency_public_id": str(self.currency.public_id)
        }
        response = self.client.post(url, data)
        BimaCoreCountry.objects.get(code=self.country.code)
        self.assertEqual(BimaCoreCountry.objects.count(), 1)
        self.assertEqual(response.status_code, 400)

    def create_permissions(self):
        permission_list = [
            ('core.country.can_create', 'Can create country'),
            ('core.country.can_update', 'Can update country'),
            ('core.country.can_delete', 'Can delete country'),
            ('core.country.can_read', 'Can read country'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaCoreCountry)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
