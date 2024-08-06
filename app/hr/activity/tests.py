from django.utils import timezone
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory
from .factories import BimaHrActivityFactory
from .models import BimaHrActivity
from hr.activity_type.factories import BimaHrActivityTypeFactory
from hr.employee.factories import BimaHrEmployeeFactory


class BimaHrActivityTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.activity_type = BimaHrActivityTypeFactory.create()
        self.employee = BimaHrEmployeeFactory.create()
        self.activity_data = {
            'name': "Activité de test",
            'description': "Ceci est une description de l'activité de test.",
            'status': "IN_PROGRESS",
            'start_date': '2023-10-01',
            'end_date': '2023-10-04',
            'activity_type_public_id': str(self.activity_type.public_id),
            'organizer_public_id': str(self.employee.public_id),
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='hr.activity.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.activity.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.activity.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.activity.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_activity(self):
        url = reverse('hr:bimahractivity-list')
        response = self.client.post(url, self.activity_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaHrActivity.objects.count(), 1)

    def test_get_activities(self):
        BimaHrActivityFactory.create_batch(5)
        url = reverse('hr:bimahractivity-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_activity(self):
        activity = BimaHrActivityFactory()
        url = reverse('hr:bimahractivity-detail', kwargs={'pk': str(activity.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaHrActivity.objects.get(pk=activity.pk).name, 'Updated Name')

    def test_delete_activity(self):
        activity = BimaHrActivityFactory()
        url = reverse('hr:bimahractivity-detail', kwargs={'pk': str(activity.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('hr:bimahractivity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('hr:bimahractivity-list')
        response = self.client.post(url, self.activity_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        activity_type = BimaHrActivityFactory()
        url = reverse('hr:bimahractivity-detail', kwargs={'pk': str(activity_type.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        activity = BimaHrActivityFactory()
        url = reverse('hr:bimahractivity-detail', kwargs={'pk': str(activity.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('hr.activity.can_create', 'Can create activity'),
            ('hr.activity.can_update', 'Can update activity'),
            ('hr.activity.can_delete', 'Can delete activity'),
            ('hr.activity.can_read', 'Can read activity'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaHrActivity)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
