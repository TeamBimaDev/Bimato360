from core.department.factories import BimaCoreDepartmentFactory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory

from .factories import BimaHrPositionFactory
from .models import BimaHrPosition
from hr.job_category.factories import BimaHrJobCategoryFactory
from hr.employee.factories import BimaHrEmployeeFactory


class BimaHrPositionTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.department = BimaCoreDepartmentFactory.create()
        self.job_category = BimaHrJobCategoryFactory.create()
        self.manager = BimaHrEmployeeFactory.create()
        self.position_data = {
            "title": "my-test-post",
            "description": "post",
            "work_location": "work_location1",
            "seniority": "JUNIOR",
            "requirements": "requirements1",
            "responsibilities": "responsibilities1",
            "department_public_id": str(self.department.public_id),
            "job_category_public_id": str(self.job_category.public_id),
            "manager_public_id": str(self.manager.public_id),
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='hr.position.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.position.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.position.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.position.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_position(self):
        url = reverse('hr:bimahrposition-list')
        response = self.client.post(url, self.position_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_positions(self):
        BimaHrPositionFactory.create_batch(5)
        url = reverse('hr:bimahrposition-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_position(self):
        position = BimaHrPositionFactory()
        url = reverse('hr:bimahrposition-detail', kwargs={'pk': str(position.public_id)})
        data = {'title': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaHrPosition.objects.get(pk=position.pk).title, 'Updated Name')

    def test_delete_position(self):
        position = BimaHrPositionFactory()
        url = reverse('hr:bimahrposition-detail', kwargs={'pk': str(position.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('hr:bimahrposition-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('hr:bimahrposition-list')
        response = self.client.post(url, self.position_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        position = BimaHrPositionFactory()
        url = reverse('hr:bimahrposition-detail', kwargs={'pk': str(position.public_id)})
        data = {'title': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        position = BimaHrPositionFactory()
        url = reverse('hr:bimahrposition-detail', kwargs={'pk': str(position.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('hr.position.can_create', 'Can create position'),
            ('hr.position.can_update', 'Can update position'),
            ('hr.position.can_delete', 'Can delete position'),
            ('hr.position.can_read', 'Can read position'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaHrPosition)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
