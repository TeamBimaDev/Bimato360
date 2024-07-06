from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .factories import BimaCoreSourceFactory
from .models import BimaCoreSource
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory


class BimaCoreSourceTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()

        self.source_data = {
            "name": "my-test-source",
            "description": "source1",
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='core.source.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.source.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.source.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.source.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_source(self):
        url = reverse('core:bimacoresource-list')
        response = self.client.post(url, self.source_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreSource.objects.count(), 1)

    def test_get_sources(self):
        BimaCoreSourceFactory.create_batch(5)
        url = reverse('core:bimacoresource-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_source(self):
        source = BimaCoreSourceFactory()
        url = reverse('core:bimacoresource-detail', kwargs={'pk': str(source.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaCoreSource.objects.get(pk=source.pk).name, 'Updated Name')

    def test_delete_source(self):
        source = BimaCoreSourceFactory()
        url = reverse('core:bimacoresource-detail', kwargs={'pk': str(source.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('core:bimacoresource-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('core:bimacoresource-list')
        response = self.client.post(url, self.source_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        source = BimaCoreSourceFactory()
        url = reverse('core:bimacoresource-detail', kwargs={'pk': str(source.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        source = BimaCoreSourceFactory()
        url = reverse('core:bimacoresource-detail', kwargs={'pk': str(source.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('core.source.can_create', 'Can create source'),
            ('core.source.can_update', 'Can update source'),
            ('core.source.can_delete', 'Can delete source'),
            ('core.source.can_read', 'Can read source'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaCoreSource)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )