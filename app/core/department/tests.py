<<<<<<< HEAD
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .factories import BimaCoreDepartmentFactory
from .models import BimaCoreDepartment
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory


class BimaCoreDepartmentTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.department_data = {
            "name": "my-test-department",
            "description": "department",
            "manager": 1,
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='core.department.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.department.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.department.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.department.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_department(self):
        url = reverse('core:bimacoredepartment-list')
        response = self.client.post(url, self.department_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreDepartment.objects.count(), 1)

    def test_create_department_with_sub_department(self):
        self.department = BimaCoreDepartmentFactory.create()
        department_data = {
            "name": "my-test-department1",
            "description": "department1",
            "manager": 2,
            "department_public_id": str(self.department.public_id),
        }
        url = reverse('core:bimacoredepartment-list')
        response = self.client.post(url, department_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreDepartment.objects.count(), 2)

    def test_get_departments(self):
        BimaCoreDepartmentFactory.create_batch(5)
        url = reverse('core:bimacoredepartment-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_department(self):
        department = BimaCoreDepartmentFactory()
        url = reverse('core:bimacoredepartment-detail', kwargs={'pk': str(department.public_id)})
        data = {'name': 'Updated Name',
                "id": str(department.public_id)
                }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaCoreDepartment.objects.get(pk=department.pk).name, 'Updated Name')

    def test_delete_department(self):
        department = BimaCoreDepartmentFactory()
        url = reverse('core:bimacoredepartment-detail', kwargs={'pk': str(department.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('core:bimacoredepartment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('core:bimacoredepartment-list')
        response = self.client.post(url, self.department_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        department = BimaCoreDepartmentFactory()
        url = reverse('core:bimacoredepartment-detail', kwargs={'pk': str(department.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        department = BimaCoreDepartmentFactory()
        url = reverse('core:bimacoredepartment-detail', kwargs={'pk': str(department.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('core.department.can_create', 'Can create department'),
            ('core.department.can_update', 'Can update department'),
            ('core.department.can_delete', 'Can delete department'),
            ('core.department.can_read', 'Can read department'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaCoreDepartment)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
=======
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .factories import BimaCoreDepartmentFactory
from .models import BimaCoreDepartment
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory


class BimaCoreDepartmentTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.department_data = {
            "name": "my-test-department",
            "description": "department",
            "manager": 1,
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='core.department.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.department.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.department.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.department.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_department(self):
        url = reverse('core:bimacoredepartment-list')
        response = self.client.post(url, self.department_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreDepartment.objects.count(), 1)

    def test_create_department_with_sub_department(self):
        self.department = BimaCoreDepartmentFactory.create()
        department_data = {
            "name": "my-test-department1",
            "description": "department1",
            "manager": 2,
            "department_public_id": str(self.department.public_id),
        }
        url = reverse('core:bimacoredepartment-list')
        response = self.client.post(url, department_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreDepartment.objects.count(), 2)

    def test_get_departments(self):
        BimaCoreDepartmentFactory.create_batch(5)
        url = reverse('core:bimacoredepartment-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_department(self):
        department = BimaCoreDepartmentFactory()
        url = reverse('core:bimacoredepartment-detail', kwargs={'pk': str(department.public_id)})
        data = {'name': 'Updated Name',
                "id": str(department.public_id)
                }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaCoreDepartment.objects.get(pk=department.pk).name, 'Updated Name')

    def test_delete_department(self):
        department = BimaCoreDepartmentFactory()
        url = reverse('core:bimacoredepartment-detail', kwargs={'pk': str(department.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('core:bimacoredepartment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('core:bimacoredepartment-list')
        response = self.client.post(url, self.department_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        department = BimaCoreDepartmentFactory()
        url = reverse('core:bimacoredepartment-detail', kwargs={'pk': str(department.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        department = BimaCoreDepartmentFactory()
        url = reverse('core:bimacoredepartment-detail', kwargs={'pk': str(department.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('core.department.can_create', 'Can create department'),
            ('core.department.can_update', 'Can update department'),
            ('core.department.can_delete', 'Can delete department'),
            ('core.department.can_read', 'Can read department'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaCoreDepartment)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
>>>>>>> origin/ma-branch
