from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .factories import BimaErpCategoryFactory
from .models import BimaErpCategory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory


class BimaErpCategoryTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.category = BimaErpCategoryFactory.create()

        self.category_data = {
            'name': 'Test category',
            'description': 'test@test.com',
            'active': True,
            "category": str(self.category.public_id)
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='erp.category.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='erp.category.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='erp.category.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='erp.category.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_category(self):
        url = reverse('erp:bimaerpcategory-list')
        response = self.client.post(url, self.category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaErpCategory.objects.count(), 2)

    def test_get_categorys(self):
        BimaErpCategoryFactory.create_batch(5)
        url = reverse('erp:bimaerpcategory-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 6)
        self.assertEqual(len(response.data['results']), 6)

    def test_update_category(self):
        category = BimaErpCategoryFactory()
        url = reverse('erp:bimaerpcategory-detail', kwargs={'pk': str(category.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaErpCategory.objects.get(pk=category.pk).name, 'Updated Name')

    def test_delete_category(self):
        category = BimaErpCategoryFactory()
        url = reverse('erp:bimaerpcategory-detail', kwargs={'pk': str(category.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('erp:bimaerpcategory-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('erp:bimaerpcategory-list')
        response = self.client.post(url, self.category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        category = BimaErpCategoryFactory()
        url = reverse('erp:bimaerpcategory-detail', kwargs={'pk': str(category.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        category = BimaErpCategoryFactory()
        url = reverse('erp:bimaerpcategory-detail', kwargs={'pk': str(category.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('erp.category.can_create', 'Can create category'),
            ('erp.category.can_update', 'Can update category'),
            ('erp.category.can_delete', 'Can delete category'),
            ('erp.category.can_read', 'Can read category'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaErpCategory)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )