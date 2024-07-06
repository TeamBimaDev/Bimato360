from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory

from .factories import BimaHrEmployeeFactory
from .models import BimaHrEmployee
from hr.employee.factories import BimaHrEmployeeFactory

from hr.position.factories import BimaHrPositionFactory


class BimaHrPositionTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.position = BimaHrPositionFactory.create()
        self.employee_data = {
            "gender": "MALE",
            "first_name": "mohamed",
            "last_name": "rh",
            "employment_type": "PERMANENT",
            "work_mode": "ONSITE",
            "job_type": "FULL_TIME",
            "employment_status": "ACTIVE",
            "hiring_date": "2023-10-01",
            "probation_end_date": "2024-04-01",
            "last_performance_review": "2024-03-15",
            "salary": 55000.789,
            "position_public_id": str(self.position.public_id),
            "balance_vacation": 10,
            "virtual_balance_vacation": 5,
            "user_public_id": str(self.user.public_id),
        }

        permission = Permission.objects.get(codename='hr.employee.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.employee.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.employee.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.employee.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_employee(self):
        url = reverse('hr:bimahremployee-list')
        response = self.client.post(url, self.employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaHrEmployee.objects.count(), 1)

    def test_get_employees(self):
        BimaHrEmployeeFactory.create_batch(5)
        url = reverse('hr:bimahremployee-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_employee(self):
        employee = BimaHrEmployeeFactory()
        url = reverse('hr:bimahremployee-detail', kwargs={'pk': str(employee.public_id)})
        data = {'employment_type': 'TEMPORARY'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaHrEmployee.objects.get(pk=employee.pk).employment_type, 'TEMPORARY')

    def test_delete_employee(self):
        employee = BimaHrEmployeeFactory()
        url = reverse('hr:bimahremployee-detail', kwargs={'pk': str(employee.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('hr:bimahremployee-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('hr:bimahremployee-list')
        response = self.client.post(url, self.employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        employee = BimaHrEmployeeFactory()
        url = reverse('hr:bimahremployee-detail', kwargs={'pk': str(employee.public_id)})
        data = {'employment_type': 'TEMPORARY'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        employee = BimaHrEmployeeFactory()
        url = reverse('hr:bimahremployee-detail', kwargs={'pk': str(employee.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('hr.employee.can_create', 'Can create employee'),
            ('hr.employee.can_update', 'Can update employee'),
            ('hr.employee.can_delete', 'Can delete employee'),
            ('hr.employee.can_read', 'Can read employee'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaHrEmployee)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
