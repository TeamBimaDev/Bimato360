from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .factories import BimaCoreTagFactory
from .models import BimaCoreTag
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory


class BimaCoreTagTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.tag = BimaCoreTagFactory.create()

        self.tag_data = {
            "name": "my-test-tag",
            "color": "1A2B3C",
            "parent": str(self.tag.public_id),
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='core.tag.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.tag.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.tag.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.tag.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_tag(self):
        url = reverse('core:bimacoretag-list')
        response = self.client.post(url, self.tag_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreTag.objects.count(), 2)

    def test_get_tags(self):
        BimaCoreTagFactory.create_batch(5)
        url = reverse('core:bimacoretag-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 6)
        self.assertEqual(len(response.data['results']), 6)

    def test_update_tag(self):
        tag = BimaCoreTagFactory()
        url = reverse('core:bimacoretag-detail', kwargs={'pk': str(tag.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaCoreTag.objects.get(pk=tag.pk).name, 'Updated Name')

    def test_delete_tag(self):
        tag = BimaCoreTagFactory()
        url = reverse('core:bimacoretag-detail', kwargs={'pk': str(tag.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('core:bimacoretag-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('core:bimacoretag-list')
        response = self.client.post(url, self.tag_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        tag = BimaCoreTagFactory()
        url = reverse('core:bimacoretag-detail', kwargs={'pk': str(tag.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        tag = BimaCoreTagFactory()
        url = reverse('core:bimacoretag-detail', kwargs={'pk': str(tag.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('core.tag.can_create', 'Can create tag'),
            ('core.tag.can_update', 'Can update tag'),
            ('core.tag.can_delete', 'Can delete tag'),
            ('core.tag.can_read', 'Can read tag'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaCoreTag)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )