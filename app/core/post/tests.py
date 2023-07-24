from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .factories import BimaCorePostFactory
from .models import BimaCorePost
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory
from core.department.factories import BimaCoreDepartmentFactory


class BimaCorePostTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.department = BimaCoreDepartmentFactory.create()
        self.post_data = {
            "name": "my-test-post",
            "description": "post",
            "requirements": "requirements1",
            "responsibilities": "responsibilities1",
            "department_public_id": str(self.department.public_id),
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='core.post.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.post.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.post.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.post.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_post(self):
        url = reverse('core:bimacorepost-list')
        response = self.client.post(url, self.post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCorePost.objects.count(), 1)

    def test_get_posts(self):
        BimaCorePostFactory.create_batch(5)
        url = reverse('core:bimacorepost-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_post(self):
        post = BimaCorePostFactory()
        url = reverse('core:bimacorepost-detail', kwargs={'pk': str(post.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaCorePost.objects.get(pk=post.pk).name, 'Updated Name')

    def test_delete_post(self):
        post = BimaCorePostFactory()
        url = reverse('core:bimacorepost-detail', kwargs={'pk': str(post.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('core:bimacorepost-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('core:bimacorepost-list')
        response = self.client.post(url, self.post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        post = BimaCorePostFactory()
        url = reverse('core:bimacorepost-detail', kwargs={'pk': str(post.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        post = BimaCorePostFactory()
        url = reverse('core:bimacorepost-detail', kwargs={'pk': str(post.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('core.post.can_create', 'Can create post'),
            ('core.post.can_update', 'Can update post'),
            ('core.post.can_delete', 'Can delete post'),
            ('core.post.can_read', 'Can read post'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaCorePost)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )