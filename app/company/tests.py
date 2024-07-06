from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .factories import BimaCompanyFactory
from .models import BimaCompany
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory
from core.currency.factories import BimaCoreCurrencyFactory


class BimaCompanyTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.currency = BimaCoreCurrencyFactory.create()

        self.company_data = {
            "name": "Acme Corporation",
            "email": "info@acme.com",
            "phone": "+1 123-456-7890",
            "mobile": "+1 987-654-3210",
            "fax": "+1 555-555-5555",
            "website": "http://www.acme.com",
            "language": "EN",
            "currency_public_id": str(self.currency.public_id),
            "timezone": "America/New_York",
            "header_note": "Welcome to Acme Corporation",
            "footer_note": "Thank you for choosing Acme Corporation",

        }
        # Give permissions to the user.
        permission = Permission.objects.get(codename='company.company.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='company.company.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='company.company.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='company.company.can_delete')
        self.user.user_permissions.add(permission)
        self.client.force_authenticate(self.user)

    def test_create_company(self):
        url = reverse('bimacompany-list')
        response = self.client.post(url, self.company_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCompany.objects.count(), 1)

    def test_get_companys(self):
        BimaCompanyFactory.create_batch(5)
        url = reverse('bimacompany-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_company(self):
        company = BimaCompanyFactory()
        url = reverse('bimacompany-detail', kwargs={'pk': str(company.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaCompany.objects.get(pk=company.pk).name, 'Updated Name')

    def test_delete_company(self):
        company = BimaCompanyFactory.create()
        url = reverse('bimacompany-detail', kwargs={'pk': str(company.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('bimacompany-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('bimacompany-list')
        response = self.client.post(url, self.company_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        company = BimaCompanyFactory()
        url = reverse('bimacompany-detail', kwargs={'pk': str(company.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        company = BimaCompanyFactory()
        url = reverse('bimacompany-detail', kwargs={'pk': str(company.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('company.company.can_create', 'Can create company'),
            ('company.company.can_update', 'Can update company'),
            ('company.company.can_delete', 'Can delete company'),
            ('company.company.can_read', 'Can read company'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaCompany)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
