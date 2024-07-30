from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory

from .factories import BimaHrQuestionFactory
from .models import BimaHrQuestion
from hr.question_category.factories import BimaHrQuestionCategoryFactory


class BimaHrPositionTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.question_category = BimaHrQuestionCategoryFactory.create()
        self.question_data = {
            "question": "Question ",
            "question_category_public_id": str(self.question_category.public_id),
            "active": True,
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='hr.question.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.question.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.question.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.question.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_question(self):
        url = reverse('hr:bimahrquestion-list')
        response = self.client.post(url, self.question_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaHrQuestion.objects.count(), 1)

    def test_get_questions(self):
        BimaHrQuestionFactory.create_batch(5)
        url = reverse('hr:bimahrquestion-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_question(self):
        question = BimaHrQuestionFactory()
        url = reverse('hr:bimahrquestion-detail', kwargs={'pk': str(question.public_id)})
        data = {'question': 'Updated question'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaHrQuestion.objects.get(pk=question.pk).question, 'Updated question')

    def test_delete_question(self):
        question = BimaHrQuestionFactory()
        url = reverse('hr:bimahrquestion-detail', kwargs={'pk': str(question.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('hr:bimahrquestion-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('hr:bimahrquestion-list')
        response = self.client.post(url, self.question_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        question = BimaHrQuestionFactory()
        url = reverse('hr:bimahrquestion-detail', kwargs={'pk': str(question.public_id)})
        data = {'question': 'Updated question'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        question = BimaHrQuestionFactory()
        url = reverse('hr:bimahrquestion-detail', kwargs={'pk': str(question.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_question(self):
        question_category = BimaHrQuestionCategoryFactory.create()
        question = BimaHrQuestionFactory.create(question_category=question_category)
        url = reverse('hr:bimahrquestion-get-question', kwargs={'category_name': question_category.name})
        print(url)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('hr.question.can_create', 'Can create question'),
            ('hr.question.can_update', 'Can update question'),
            ('hr.question.can_delete', 'Can delete question'),
            ('hr.question.can_read', 'Can read question'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaHrQuestion)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
