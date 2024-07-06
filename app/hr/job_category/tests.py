from core.department.factories import BimaCoreDepartmentFactory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory

from .factories import BimaHrJobCategoryFactory
from .models import BimaHrJobCategory


class BimaHrJobCategoryTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.job_category_data = {
            "name": "job_category",
            "description": "description1",
            "active": True,
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='hr.job_category.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.job_category.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.job_category.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.job_category.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_post(self):
        url = reverse('hr:bimahrjobcategory-list')
        response = self.client.post(url, self.job_category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaHrJobCategory.objects.count(), 1)

    def test_get_posts(self):
        BimaHrJobCategoryFactory.create_batch(5)
        url = reverse('hr:bimahrjobcategory-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_post(self):
        job_category = BimaHrJobCategoryFactory()
        url = reverse('hr:bimahrjobcategory-detail', kwargs={'pk': str(job_category.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaHrJobCategory.objects.get(pk=job_category.pk).name, 'Updated Name')

    def test_delete_post(self):
        job_category = BimaHrJobCategoryFactory()
        url = reverse('hr:bimahrjobcategory-detail', kwargs={'pk': str(job_category.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('hr:bimahrjobcategory-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('hr:bimahrjobcategory-list')
        response = self.client.post(url, self.job_category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        job_category = BimaHrJobCategoryFactory()
        url = reverse('hr:bimahrjobcategory-detail', kwargs={'pk': str(job_category.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        job_category = BimaHrJobCategoryFactory()
        url = reverse('hr:bimahrjobcategory-detail', kwargs={'pk': str(job_category.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('hr.job_category.can_create', 'Can create job category'),
            ('hr.job_category.can_update', 'Can update job category'),
            ('hr.job_category.can_delete', 'Can delete job category'),
            ('hr.job_category.can_read', 'Can read job category'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaHrJobCategory)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
