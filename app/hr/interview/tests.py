from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory
from .factories import BimaHrInterviewFactory
from .models import BimaHrInterview
from hr.vacancie.factories import BimaHrVacancieFactory
from hr.candidat.factories import BimaHrCandidatFactory
from hr.interview_step.factories import BimaHrInterviewStepFactory

class BimaHrInterviewStepTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()

        # Give permissions to the user.
        permission = Permission.objects.get(codename='hr.interview.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.interview.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.interview.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.interview.can_delete')
        self.user.user_permissions.add(permission)      
        self.client.force_authenticate(self.user)

    def create_permissions(self):
        permission_list = [
            ('hr.interview.can_create', 'Can create interview '),
            ('hr.interview.can_update', 'Can update interview '),
            ('hr.interview.can_delete', 'Can delete interview '),
            ('hr.interview.can_read', 'Can read interview '),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaHrInterview)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )

    def test_create_interview(self):
        url = reverse('hr:bimahrinterview-list')
        vacancie = BimaHrVacancieFactory.create()
        candidat = BimaHrCandidatFactory.create()
        interview_step = BimaHrInterviewStepFactory.create()
        interview_data = {
            "name": "Interview Name",
            "due_date": "Two_Day",
            "score": 85,
            "status": "PLANNED",
            "candidat_public_id": candidat.public_id,
            "vacancie_public_id": vacancie.public_id,
            "link_interview": "http://example.com/interview",
            "estimated_time": "Half_hour",
            "interview_step_public_id":interview_step.public_id,
            "comments": "Initial interview"
        }
        response = self.client.post(url, interview_data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaHrInterview.objects.count(), 1)

    def test_get_interviews(self):
        BimaHrInterviewFactory.create_batch(5)
        url = reverse('hr:bimahrinterview-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)


    def test_update_interview(self):
        interview = BimaHrInterviewFactory()
        url = reverse('hr:bimahrinterview-detail', kwargs={'pk': str(interview.public_id)})
        updated_data = {"name": "Updated Interview Name"}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaHrInterview.objects.get(pk=interview.pk).name, "Updated Interview Name")

    def test_delete_interview(self):
        interview = BimaHrInterviewFactory()
        url = reverse('hr:bimahrinterview-detail', kwargs={'pk': str(interview.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_unauthenticated_access(self):
        self.client.logout()
        url = reverse('hr:bimahrinterview-list') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('hr:bimahrinterview-list')  
        vacancie = BimaHrVacancieFactory.create()
        candidat = BimaHrCandidatFactory.create()
        interview_step = BimaHrInterviewStepFactory.create()
        interview_data = {
            "name": "Interview Name",
            "due_date": "Two_Day",
            "score": 85,
            "status": "PLANNED",
            "candidat_public_id": candidat.public_id,
            "vacancie_public_id": vacancie.public_id,
            "link_interview": "http://example.com/interview",
            "estimated_time": "Half_hour",
            "interview_step_public_id":interview_step.public_id,
            "comments": "Initial interview"
        }
        response = self.client.post(url, interview_data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        interview = BimaHrInterviewFactory()  
        url = reverse('hr:bimahrinterview-detail', kwargs={'pk': str(interview.public_id)})  
        updated_data = {"name": "Updated Interview Name"}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        interview = BimaHrInterviewFactory()  
        url = reverse('hr:bimahrinterview-detail', kwargs={'pk': str(interview.public_id)})  
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

