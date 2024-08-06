<<<<<<< HEAD
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory
from .factories import BimaHrActivityTypeFactory
from .models import BimaHrActivityType


class BimaHrActivityTypeTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.activity_type_data = {
            "name": "my-test-activity-type",
            "description": "activity_type",
            "active": True,
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='hr.activity_type.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.activity_type.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.activity_type.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.activity_type.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_activity_type(self):
        url = reverse('hr:bimahractivitytype-list')
        response = self.client.post(url, self.activity_type_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaHrActivityType.objects.count(), 1)

    def test_get_activities_type(self):
        BimaHrActivityTypeFactory.create_batch(5)
        url = reverse('hr:bimahractivitytype-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_activity_type(self):
        activity_type = BimaHrActivityTypeFactory()
        url = reverse('hr:bimahractivitytype-detail', kwargs={'pk': str(activity_type.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaHrActivityType.objects.get(pk=activity_type.pk).name, 'Updated Name')

    def test_delete_activity_type(self):
        activity_type = BimaHrActivityTypeFactory()
        url = reverse('hr:bimahractivitytype-detail', kwargs={'pk': str(activity_type.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('hr:bimahractivitytype-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('hr:bimahractivitytype-list')
        response = self.client.post(url, self.activity_type_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        activity_type = BimaHrActivityTypeFactory()
        url = reverse('hr:bimahractivitytype-detail', kwargs={'pk': str(activity_type.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        activity_type = BimaHrActivityTypeFactory()
        url = reverse('hr:bimahractivitytype-detail', kwargs={'pk': str(activity_type.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('hr.activity_type.can_create', 'Can create activity type'),
            ('hr.activity_type.can_update', 'Can update activity type'),
            ('hr.activity_type.can_delete', 'Can delete activity type'),
            ('hr.activity_type.can_read', 'Can read activity type'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaHrActivityType)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
=======
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory
from .factories import BimaHrActivityTypeFactory
from .models import BimaHrActivityType


class BimaHrActivityTypeTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.activity_type_data = {
            "name": "my-test-activity-type",
            "description": "activity_type",
            "active": True,
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='hr.activity_type.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.activity_type.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.activity_type.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.activity_type.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_activity_type(self):
        url = reverse('hr:bimahractivitytype-list')
        response = self.client.post(url, self.activity_type_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaHrActivityType.objects.count(), 1)

    def test_get_activities_type(self):
        BimaHrActivityTypeFactory.create_batch(5)
        url = reverse('hr:bimahractivitytype-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_activity_type(self):
        activity_type = BimaHrActivityTypeFactory()
        url = reverse('hr:bimahractivitytype-detail', kwargs={'pk': str(activity_type.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaHrActivityType.objects.get(pk=activity_type.pk).name, 'Updated Name')

    def test_delete_activity_type(self):
        activity_type = BimaHrActivityTypeFactory()
        url = reverse('hr:bimahractivitytype-detail', kwargs={'pk': str(activity_type.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('hr:bimahractivitytype-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('hr:bimahractivitytype-list')
        response = self.client.post(url, self.activity_type_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        activity_type = BimaHrActivityTypeFactory()
        url = reverse('hr:bimahractivitytype-detail', kwargs={'pk': str(activity_type.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        activity_type = BimaHrActivityTypeFactory()
        url = reverse('hr:bimahractivitytype-detail', kwargs={'pk': str(activity_type.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('hr.activity_type.can_create', 'Can create activity type'),
            ('hr.activity_type.can_update', 'Can update activity type'),
            ('hr.activity_type.can_delete', 'Can delete activity type'),
            ('hr.activity_type.can_read', 'Can read activity type'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaHrActivityType)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
>>>>>>> origin/ma-branch
