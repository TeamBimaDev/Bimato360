'''# technical interview_question/tests.py
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory
from .factories import BimaHrInterviewQuestionFactory
from hr.interview.factories import BimaHrInterviewFactory
from .models import BimaHrInterviewQuestion

class BimaHrInterviewQuestionTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()

        # Give permissions to the user.
        permission = Permission.objects.get(codename='hr.interview_question.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.interview_question.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.interview_question.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.interview_question.can_delete')
        self.user.user_permissions.add(permission)
        self.client.force_authenticate(self.user)

    def create_permissions(self):
        permission_list = [
            ('hr.interview_question.can_create', 'Can create interview question'),
            ('hr.interview_question.can_update', 'Can update interview question'),
            ('hr.interview_question.can_delete', 'Can delete interview question'),
            ('hr.interview_question.can_read', 'Can read interview question'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaHrInterviewQuestion)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )

    def test_create_interview_question(self):
        url = reverse('hr:bimahrinterviewquestion-list')
        interview = BimaHrInterviewFactory.create()
        interview_question_data = {
            "question": "What is your greatest strength?",
            "response": "I am very detail-oriented.",
            "interview_public_id": interview.public_id,
        }
        response = self.client.post(url, interview_question_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaHrInterviewQuestion.objects.count(), 1)

    def test_get_interview_questions(self):
        BimaHrInterviewQuestionFactory.create_batch(5)
        url = reverse('hr:bimahrinterviewquestion-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_interview_question(self):
        interview_question = BimaHrInterviewQuestionFactory()
        url = reverse('hr:bimahrinterviewquestion-detail', kwargs={'pk': str(interview_question.public_id)})
        updated_data = {"question": "What is your greatest weakness?"}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaHrInterviewQuestion.objects.get(pk=interview_question.pk).question, "What is your greatest weakness?")

    def test_delete_interview_question(self):
        interview_question = BimaHrInterviewQuestionFactory()
        url = reverse('hr:bimahrinterviewquestion-detail', kwargs={'pk': str(interview_question.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_access(self):
        self.client.logout()
        url = reverse('hr:bimahrinterviewquestion-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('hr:bimahrinterviewquestion-list')
        interview = BimaHrInterviewFactory.create()
        interview_question_data = {
            "question": "What is your greatest strength?",
            "response": "I am very detail-oriented.",
            "interview_public_id": interview.public_id,
        }
        response = self.client.post(url, interview_question_data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        interview_question = BimaHrInterviewQuestionFactory()
        url = reverse('hr:bimahrinterviewquestion-detail', kwargs={'pk': str(interview_question.public_id)})
        updated_data = {"question": "What is your greatest weakness?"}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        interview_question = BimaHrInterviewQuestionFactory()
        url = reverse('hr:bimahrinterviewquestion-detail', kwargs={'pk': str(interview_question.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
'''