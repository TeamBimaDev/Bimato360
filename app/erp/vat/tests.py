from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .factories import BimaErpVatFactory
from .models import BimaErpVat
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory


class BimaErpVatTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.vat_data = {
            "name": "erpvat1",
            "rate": 2222,
            "active": True,
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='erp.vat.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='erp.vat.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='erp.vat.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='erp.vat.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_vat(self):
        url = reverse('erp:bimaerpvat-list')
        response = self.client.post(url, self.vat_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaErpVat.objects.count(), 1)

    def test_get_vats(self):
        BimaErpVatFactory.create_batch(5)
        url = reverse('erp:bimaerpvat-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_vat(self):
        vat = BimaErpVatFactory()
        url = reverse('erp:bimaerpvat-detail', kwargs={'pk': str(vat.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaErpVat.objects.get(pk=vat.pk).name, 'Updated Name')

    def test_delete_vat(self):
        vat = BimaErpVatFactory()
        url = reverse('erp:bimaerpvat-detail', kwargs={'pk': str(vat.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('erp:bimaerpvat-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('erp:bimaerpcategory-list')
        response = self.client.post(url, self.vat_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        vat = BimaErpVatFactory()
        url = reverse('erp:bimaerpcategory-detail', kwargs={'pk': str(vat.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        vat = BimaErpVatFactory()
        url = reverse('erp:bimaerpvat-detail', kwargs={'pk': str(vat.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('erp.vat.can_create', 'Can create vat'),
            ('erp.vat.can_update', 'Can update vat'),
            ('erp.vat.can_delete', 'Can delete vat'),
            ('erp.vat.can_read', 'Can read vat'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaErpVat)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )