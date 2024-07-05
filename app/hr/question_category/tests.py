from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory

from .factories import BimaHrQuestionCategoryFactory
from .models import BimaHrQuestionCategory


class BimaHrQuestionCategoryTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.question_category_data = {
            "name": "Category Name",
            "description": "This is a description of the category.",
            "active": True,
            "category": None,
        }
        
        # Give permissions to the user.
        permission = Permission.objects.get(codename='hr.question_category.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.question_category.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.question_category.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.question_category.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_question_category(self):
        url = reverse('hr:bimahrquestioncategory-list')
        response = self.client.post(url, self.question_category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaHrQuestionCategory.objects.count(), 1)

    def test_get_questions_category(self):
        BimaHrQuestionCategoryFactory.create_batch(5)
        url = reverse('hr:bimahrquestioncategory-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_question_category(self):
        question_category = BimaHrQuestionCategoryFactory()
        url = reverse('hr:bimahrquestioncategory-detail', kwargs={'pk': str(question_category.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaHrQuestionCategory.objects.get(pk=question_category.pk).name, 'Updated Name')

    def test_delete_question_category(self):
        question_category = BimaHrQuestionCategoryFactory()
        url = reverse('hr:bimahrquestioncategory-detail', kwargs={'pk': str(question_category.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('hr:bimahrquestioncategory-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('hr:bimahrquestioncategory-list')
        response = self.client.post(url, self.question_category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        question_category = BimaHrQuestionCategoryFactory()
        url = reverse('hr:bimahrquestioncategory-detail', kwargs={'pk': str(question_category.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        question_category = BimaHrQuestionCategoryFactory()
        url = reverse('hr:bimahrquestioncategory-detail', kwargs={'pk': str(question_category.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('hr.question_category.can_create', 'Can create question category'),
            ('hr.question_category.can_update', 'Can update question category'),
            ('hr.question_category.can_delete', 'Can delete question category'),
            ('hr.question_category.can_read', 'Can read question category'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaHrQuestionCategory)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )

