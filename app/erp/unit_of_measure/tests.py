from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .factories import BimaErpUnitOfMeasureFactory
from .models import BimaErpUnitOfMeasure
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory


class BimaErpUnitOfMeasureTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()

        self.unit_of_measure_data = {
            "name": "BimaErpUnitOfMeasure_test",
            "active": True,
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='erp.unit_of_measure.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='erp.unit_of_measure.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='erp.unit_of_measure.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='erp.unit_of_measure.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_unit_of_measure(self):
        url = reverse('erp:bimaerpunitofmeasure-list')
        response = self.client.post(url, self.unit_of_measure_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaErpUnitOfMeasure.objects.count(), 1)

    def test_get_units_of_measure(self):
        BimaErpUnitOfMeasureFactory.create_batch(5)
        url = reverse('erp:bimaerpunitofmeasure-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_unit_of_measure(self):
        unit_of_measure = BimaErpUnitOfMeasureFactory()
        url = reverse('erp:bimaerpunitofmeasure-detail', kwargs={'pk': str(unit_of_measure.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaErpUnitOfMeasure.objects.get(pk=unit_of_measure.pk).name, 'Updated Name')

    def test_delete_unit_of_measure(self):
        unit_of_measure = BimaErpUnitOfMeasureFactory()
        url = reverse('erp:bimaerpunitofmeasure-detail', kwargs={'pk': str(unit_of_measure.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('erp:bimaerpunitofmeasure-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('erp:bimaerpunitofmeasure-list')
        response = self.client.post(url, self.unit_of_measure_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        unit_of_measure = BimaErpUnitOfMeasureFactory()
        url = reverse('erp:bimaerpunitofmeasure-detail', kwargs={'pk': str(unit_of_measure.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        unit_of_measure = BimaErpUnitOfMeasureFactory()
        url = reverse('erp:bimaerpunitofmeasure-detail', kwargs={'pk': str(unit_of_measure.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('erp.unit_of_measure.can_create', 'Can create unit of measure'),
            ('erp.unit_of_measure.can_update', 'Can update unit of measure'),
            ('erp.unit_of_measure.can_delete', 'Can delete unit of measure'),
            ('erp.unit_of_measure.can_read', 'Can read unit of measure'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaErpUnitOfMeasure)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )