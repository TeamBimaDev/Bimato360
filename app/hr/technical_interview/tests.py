from unittest.mock import patch
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from hr.position.factories import BimaHrPositionFactory
from user.factories import UserFactory
from .factories import BimaHrTechnicalInterviewFactory
from .models import BimaHrTechnicalInterview
from hr.vacancie.factories import BimaHrVacancieFactory
from hr.interview_step.factories import BimaHrInterviewStepFactory
from hr.candidat.models import BimaHrCandidat
from hr.employee.models import BimaHrEmployee

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


        # Create necessary related objects
        self.vacancie = BimaHrVacancieFactory.create()
        self.interview_step = BimaHrInterviewStepFactory.create()
        self.position = BimaHrPositionFactory.create()
        
        # Creating candidat and employee
        self.candidat = BimaHrCandidat.objects.create(
            gender="MALE",
            first_name="Mohamed",
            last_name="Amira",
            email="mohammedamineamira@gmail.com",
            phone_number="+1234567890",
            availability_days=5,
            message="Hello, I'm Mohamed Amine.",
        )
        self.employee = BimaHrEmployee.objects.create(
            gender="MALE",
            first_name="mohamed",
            last_name="rh",
            employment_type="PERMANENT",
            work_mode="ONSITE",
            job_type="FULL_TIME",
            employment_status="ACTIVE",
            hiring_date="2023-10-01",
            probation_end_date="2024-04-01",
            last_performance_review="2024-03-15",
            salary=55000.789,
            position=self.position,
            balance_vacation=10,
            virtual_balance_vacation=5,
            user=self.user,
            email="mohamedamine.bima@outlook.com",
        )

    def create_permissions(self):
        permission_list = [
            ('hr.technical_interview.can_create', 'Can create technical interview'),
            ('hr.technical_interview.can_update', 'Can update technical interview'),
            ('hr.technical_interview.can_delete', 'Can delete technical interview'),
            ('hr.technical_interview.can_read', 'Can read technical interview'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaHrTechnicalInterview)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )

    @patch('hr.technical_interview.utils.google_calendar.create_calendar_event')
    def test_create_technical_interview(self, mock_create_calendar_event):
        url = reverse('hr:bimahrtechnicalinterview-list')
        technical_interview_data = {
            "title": "Technical Interview Title",
            "description": "This is a technical interview.",
            "start_datetime": "2024-08-05T10:00:00Z",
            "end_datetime": "2024-08-05T11:00:00Z",
            "interview_mode": "ONLINE",
            "location": "Virtual",
            "candidat_public_id": self.candidat.public_id,
            "vacancie_public_id": self.vacancie.public_id,
            "interview_step_public_id": self.interview_step.public_id,
            "interviewers": [self.employee.public_id],
        }
        response = self.client.post(url, technical_interview_data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('hr.technical_interview.utils.google_calendar.create_calendar_event')
    def test_get_technical_interviews(self, mock_create_calendar_event):
        BimaHrTechnicalInterviewFactory.create_batch(5)
        url = reverse('hr:bimahrtechnicalinterview-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)
        mock_create_calendar_event.assert_not_called()

    # @patch('hr.technical_interview.utils.google_calendar.update_calendar_event')
    # def test_update_technical_interview(self, mock_update_calendar_event):
    #     technical_interview = BimaHrTechnicalInterviewFactory.create(
    #         title="Original Technical Interview Title",
    #         start_datetime="2024-08-07T10:00:00Z",
    #         end_datetime="2024-08-07T11:00:00Z",
    #     )
    #     url = reverse('hr:bimahrtechnicalinterview-detail', kwargs={'pk': str(technical_interview.public_id)})
    #     updated_data = {
    #         "title": "Updated Technical Interview Title",
    #         "description": "This is an updated technical interview.",
    #     }
    #     response = self.client.patch(url, updated_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     mock_update_calendar_event.assert_called_once()

    @patch('hr.technical_interview.utils.google_calendar.delete_calendar_event')
    def test_delete_technical_interview(self, mock_delete_calendar_event):
        technical_interview = BimaHrTechnicalInterviewFactory.create()
        url = reverse('hr:bimahrtechnicalinterview-detail', kwargs={'pk': str(technical_interview.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BimaHrTechnicalInterview.objects.count(), 0)

    @patch('hr.technical_interview.utils.google_calendar.create_calendar_event')
    @patch('hr.technical_interview.utils.google_calendar.update_calendar_event')
    @patch('hr.technical_interview.utils.google_calendar.delete_calendar_event')
    def test_unauthenticated_user(self, mock_delete_calendar_event, mock_update_calendar_event, mock_create_calendar_event):
        url = reverse('hr:bimahrtechnicalinterview-list')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        mock_create_calendar_event.assert_not_called()
        mock_update_calendar_event.assert_not_called()
        mock_delete_calendar_event.assert_not_called()

    @patch('hr.technical_interview.utils.google_calendar.update_calendar_event')
    def test_update_technical_interview_invalid_data(self, mock_update_calendar_event):
        technical_interview = BimaHrTechnicalInterviewFactory.create()
        url = reverse('hr:bimahrtechnicalinterview-detail', kwargs={'pk': str(technical_interview.public_id)})
        invalid_data = {
            "title": "",  # Invalid data
        }
        response = self.client.patch(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_update_calendar_event.assert_not_called()

    def test_unauthenticated_user(self):
        self.client.force_authenticate(user=None)
        url = reverse('hr:bimahrtechnicalinterview-list')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
