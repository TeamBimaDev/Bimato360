from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory
from .factories import BimaHrTechnicalInterviewFactory
from .models import BimaHrTechnicalInterview
from hr.vacancie.factories import BimaHrVacancieFactory
from hr.candidat.factories import BimaHrCandidatFactory
from hr.interview_step.factories import BimaHrInterviewStepFactory
from hr.employee.factories import BimaHrEmployeeFactory

class BimaHrTechnicalInterviewTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()

        # Give permissions to the user
        permission = Permission.objects.get(codename='hr.technical_interview.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.technical_interview.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.technical_interview.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.technical_interview.can_delete')
        self.user.user_permissions.add(permission)      
        self.client.force_authenticate(self.user)

    def create_permissions(self):
        permission_list = [
            ('hr.technical_interview.can_create', 'Can create technical interview '),
            ('hr.technical_interview.can_update', 'Can update technical interview '),
            ('hr.technical_interview.can_delete', 'Can delete technical interview '),
            ('hr.technical_interview.can_read', 'Can read technical interview '),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaHrTechnicalInterview)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )

    def test_create_technical_interview(self):
        url = reverse('hr:bimahrtechnicalinterview-list')
        vacancie = BimaHrVacancieFactory.create()
        candidat = BimaHrCandidatFactory.create()
        interview_step = BimaHrInterviewStepFactory.create()
        interviewer = BimaHrEmployeeFactory.create()
        technical_interview_data = {
            "title": "Technical Interview Title",
            "description": "This is a technical interview.",
            "start_datetime": "2024-08-05T10:00:00Z",
            "end_datetime": "2024-08-05T11:00:00Z",
            "interview_mode": "ONLINE",
            "location": "Virtual",
            "candidat_public_id": candidat.public_id,
            "vacancie_public_id": vacancie.public_id,
            "interview_step_public_id": interview_step.public_id,
            "interviewers": [interviewer.public_id],
        }
        response = self.client.post(url, technical_interview_data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaHrTechnicalInterview.objects.count(), 1)

    def test_get_technical_interviews(self):
        BimaHrTechnicalInterviewFactory.create_batch(5)
        url = reverse('hr:bimahrtechnicalinterview-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_technical_interview(self):
        technical_interview = BimaHrTechnicalInterviewFactory()
        url = reverse('hr:bimahrtechnicalinterview-detail', kwargs={'pk': str(technical_interview.public_id)})
        updated_data = {"title": "Updated Technical Interview Title"}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaHrTechnicalInterview.objects.get(pk=technical_interview.pk).title, "Updated Technical Interview Title")

    def test_delete_technical_interview(self):
        technical_interview = BimaHrTechnicalInterviewFactory()
        url = reverse('hr:bimahrtechnicalinterview-detail', kwargs={'pk': str(technical_interview.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BimaHrTechnicalInterview.objects.count(), 0)

    def test_unauthenticated_access(self):
        self.client.logout()
        url = reverse('hr:bimahrtechnicalinterview-list') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('hr:bimahrtechnicalinterview-list')  
        vacancie = BimaHrVacancieFactory.create()
        candidat = BimaHrCandidatFactory.create()
        interview_step = BimaHrInterviewStepFactory.create()
        technical_interview_data = {
            "title": "Technical Interview Title",
            "description": "This is a technical interview.",
            "start_datetime": "2024-08-05T10:00:00Z",
            "end_datetime": "2024-08-05T11:00:00Z",
            "interview_mode": "ONLINE",
            "location": "Virtual",
            "candidat_public_id": candidat.public_id,
            "vacancie_public_id": vacancie.public_id,
            "link_interview": "http://example.com/interview",
            "interview_step_public_id": interview_step.public_id,
        }
        response = self.client.post(url, technical_interview_data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        technical_interview = BimaHrTechnicalInterviewFactory()  
        url = reverse('hr:bimahrtechnicalinterview-detail', kwargs={'pk': str(technical_interview.public_id)})  
        updated_data = {"title": "Updated Technical Interview Title"}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        technical_interview = BimaHrTechnicalInterviewFactory()  
        url = reverse('hr:bimahrtechnicalinterview-detail', kwargs={'pk': str(technical_interview.public_id)})  
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
