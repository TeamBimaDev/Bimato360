from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory


from.factories import BimaHrCandidatFactory
from.models import BimaHrCandidat
from hr.candidat.factories import BimaHrCandidatFactory
from core.country.factories import BimaCoreCountryFactory


class BimaHrCandidatTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.country= BimaCoreCountryFactory.create()
        self.candidat_data = {
            "gender":"MALE",
            "first_name": "Mohamed",
            "last_name": "Amira",
            "country_public_id":str(self.country.public_id),
            "email": "mohamed.amira@example.com",
            "phone_number": "+1234567890",
            "availability_days": 5,
            "message": "Hello, I'm Mohamed Amine.",
        }

               
        permission = Permission.objects.get(codename='hr.candidat.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.candidat.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.candidat.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.candidat.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_candidat(self):
        url = reverse('hr:bimahrcandidat-list')
        print(url)
        response = self.client.post(url, self.candidat_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaHrCandidat.objects.count(), 1)

    def test_get_candidats(self):
        BimaHrCandidatFactory.create_batch(5)
        url = reverse('hr:bimahrcandidat-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_candidat(self):
        candidat = BimaHrCandidatFactory()
        url = reverse('hr:bimahrcandidat-detail', kwargs={'pk': str(candidat.public_id)})
        data = {'availability_days': 10}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaHrCandidat.objects.get(pk=candidat.pk).availability_days, 10)

    def test_delete_candidat(self):
        candidat = BimaHrCandidatFactory()
        url = reverse('hr:bimahrcandidat-detail', kwargs={'pk': str(candidat.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_access(self):
        self.client.logout()
        url = reverse('hr:bimahrcandidat-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        url = reverse('hr:bimahrcandidat-list')
        response = self.client.post(url, self.candidat_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        candidat = BimaHrCandidatFactory()
        url = reverse('hr:bimahrcandidat-detail', kwargs={'pk': str(candidat.public_id)})
        data = {'availability_days': 10}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        candidat = BimaHrCandidatFactory()
        url = reverse('hr:bimahrcandidat-detail', kwargs={'pk': str(candidat.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            ('hr.candidat.can_create', 'Can create candidat'),
            ('hr.candidat.can_update', 'Can update candidat'),
            ('hr.candidat.can_delete', 'Can delete candidat'),
            ('hr.candidat.can_read', 'Can read candidat'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaHrCandidat)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )

