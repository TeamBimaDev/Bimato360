from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .factories import BimaCoreStateFactory
from .models import BimaCoreState
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory
from core.country.factories import BimaCoreCountryFactory


class BimaCoreStateTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.country = BimaCoreCountryFactory.create()

        self.state_data = {
            "name": "my-test-state",
            "code": "1A2B3C",
            "country_public_id": str(self.country.public_id),
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='core.state.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.state.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.state.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.state.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_state(self):
        url = reverse('core:bimacorestate-list')
        response = self.client.post(url, self.state_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreState.objects.count(), 1)

    def test_get_states(self):
        BimaCoreStateFactory.create_batch(5)
        url = reverse('core:bimacorestate-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_state(self):
        state = BimaCoreStateFactory()
        url = reverse('core:bimacorestate-detail', kwargs={'pk': str(state.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaCoreState.objects.get(pk=state.pk).name, 'Updated Name')

    def test_delete_state(self):
        state = BimaCoreStateFactory()
        url = reverse('core:bimacorestate-detail', kwargs={'pk': str(state.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('core:bimacorestate-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('core:bimacorestate-list')
        response = self.client.post(url, self.state_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        state = BimaCoreStateFactory()
        url = reverse('core:bimacorestate-detail', kwargs={'pk': str(state.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        state = BimaCoreStateFactory()
        url = reverse('core:bimacorestate-detail', kwargs={'pk': str(state.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('core.state.can_create', 'Can create state'),
            ('core.state.can_update', 'Can update state'),
            ('core.state.can_delete', 'Can delete state'),
            ('core.state.can_read', 'Can read state'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaCoreState)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )