from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .factories import  BimaCoreCashFactory
from .models import BimaCoreCash
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory


class BimaCoreCashTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()

        self.cash_data = {
            'name': 'Test Cash',
            'active': True,
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='core.cash.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.cash.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.cash.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.cash.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_cash(self):
        url = reverse('core:bimacorecash-list')
        response = self.client.post(url, self.cash_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreCash.objects.count(), 1)

    def test_get_cashs(self):
        BimaCoreCashFactory.create_batch(5)
        url = reverse('core:bimacorecash-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_cash(self):
        cash = BimaCoreCashFactory()
        url = reverse('core:bimacorecash-detail', kwargs={'pk': str(cash.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaCoreCash.objects.get(pk=cash.pk).name, 'Updated Name')

   # def test_delete_cash(self):
    #    cash = BimaCoreCashFactory()
     #   url = reverse('core:bimacorecash-detail', kwargs={'pk': str(cash.public_id)})
      #  response = self.client.delete(url, format='json')
       # self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('core:bimacorecash-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('core:bimacorecash-list')
        response = self.client.post(url, self.cash_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        cash = BimaCoreCashFactory()
        url = reverse('core:bimacorecash-detail', kwargs={'pk': str(cash.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        cash = BimaCoreCashFactory()
        url = reverse('core:bimacorecash-detail', kwargs={'pk': str(cash.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('core.cash.can_create', 'Can create cash'),
            ('core.cash.can_update', 'Can update cash'),
            ('core.cash.can_delete', 'Can delete cash'),
            ('core.cash.can_read', 'Can read cash'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaCoreCash)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )