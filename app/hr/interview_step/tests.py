from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory
from .factories import BimaHrInterviewStepFactory
from .models import BimaHrInterviewStep

class BimaHrInterviewStepTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()

         # Give permissions to the user.
        permission = Permission.objects.get(codename='hr.interview_step.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.interview_step.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.interview_step.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.interview_step.can_delete')
        self.user.user_permissions.add(permission)      
        self.client.force_authenticate(self.user)

    def create_permissions(self):
        permission_list = [
            ('hr.interview_step.can_create', 'Can create interview step'),
            ('hr.interview_step.can_update', 'Can update interview step'),
            ('hr.interview_step.can_delete', 'Can delete interview step'),
            ('hr.interview_step.can_read', 'Can read interview step'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaHrInterviewStep)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )


    def test_create_interview_step(self):
        url = reverse('hr:bimahrinterviewstep-list')
        interview_step_data = {
            "name": "Interview Step Name",
            "interview_type": "HR",
            "description": "Description of the interview step",
            "active": True,
        }
        response = self.client.post(url, interview_step_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaHrInterviewStep.objects.count(), 1)

    def test_get_interview_steps(self):
        BimaHrInterviewStepFactory.create_batch(5)
        url = reverse('hr:bimahrinterviewstep-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_interview_step(self):
        interview_step = BimaHrInterviewStepFactory()
        url = reverse('hr:bimahrinterviewstep-detail', kwargs={'pk': str(interview_step.public_id)})
        updated_data = {"name": "Updated Interview Step Name", "description": "Updated Description"}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaHrInterviewStep.objects.get(pk=interview_step.pk).name, "Updated Interview Step Name")

    def test_delete_interview_step(self):
        interview_step = BimaHrInterviewStepFactory()
        url = reverse('hr:bimahrinterviewstep-detail', kwargs={'pk': str(interview_step.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_access(self):
        self.client.logout()
        url = reverse('hr:bimahrinterviewstep-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('hr:bimahrinterviewstep-list')
        interview_step_data = {
            "name": "Interview Step Name",
            "interview_type": "Technical Interview",
            "description": "Description of the interview step",
            "active": True,
        }
        response = self.client.post(url, interview_step_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        interview_step = BimaHrInterviewStepFactory()
        url = reverse('hr:bimahrinterviewstep-detail', kwargs={'pk': str(interview_step.public_id)})
        updated_data = {"name": "Updated Interview Step Name", "description": "Updated Description"}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        interview_step = BimaHrInterviewStepFactory()
        url = reverse('hr:bimahrinterviewstep-detail', kwargs={'pk': str(interview_step.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
