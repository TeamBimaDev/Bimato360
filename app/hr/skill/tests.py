<<<<<<< HEAD
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory

from .factories import BimaHrSkillFactory
from .models import BimaHrSkill
from hr.skill_category.factories import BimaHrSkillCategoryFactory


class BimaHrPositionTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.skill_category = BimaHrSkillCategoryFactory.create()
        self.skill_data = {
            "name": "skill Name",
            "skill_category_public_id": str(self.skill_category.public_id),
            "description": "This is a description of the skill.",
            "active": True,
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='hr.skill.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.skill.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.skill.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.skill.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_skill(self):
        url = reverse('hr:bimahrskill-list')
        response = self.client.post(url, self.skill_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaHrSkill.objects.count(), 1)

    def test_get_skills(self):
        BimaHrSkillFactory.create_batch(5)
        url = reverse('hr:bimahrskill-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_skill(self):
        skill = BimaHrSkillFactory()
        url = reverse('hr:bimahrskill-detail', kwargs={'pk': str(skill.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaHrSkill.objects.get(pk=skill.pk).name, 'Updated Name')

    def test_delete_skill(self):
        skill = BimaHrSkillFactory()
        url = reverse('hr:bimahrskill-detail', kwargs={'pk': str(skill.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('hr:bimahrskill-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('hr:bimahrskill-list')
        response = self.client.post(url, self.skill_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        skill = BimaHrSkillFactory()
        url = reverse('hr:bimahrskill-detail', kwargs={'pk': str(skill.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        skill = BimaHrSkillFactory()
        url = reverse('hr:bimahrskill-detail', kwargs={'pk': str(skill.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('hr.skill.can_create', 'Can create skill'),
            ('hr.skill.can_update', 'Can update skill'),
            ('hr.skill.can_delete', 'Can delete skill'),
            ('hr.skill.can_read', 'Can read skill'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaHrSkill)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
=======
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory

from .factories import BimaHrSkillFactory
from .models import BimaHrSkill
from hr.skill_category.factories import BimaHrSkillCategoryFactory


class BimaHrPositionTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.skill_category = BimaHrSkillCategoryFactory.create()
        self.skill_data = {
            "name": "skill Name",
            "skill_category_public_id": str(self.skill_category.public_id),
            "description": "This is a description of the skill.",
            "active": True,
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='hr.skill.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.skill.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.skill.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.skill.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_skill(self):
        url = reverse('hr:bimahrskill-list')
        response = self.client.post(url, self.skill_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaHrSkill.objects.count(), 1)

    def test_get_skills(self):
        BimaHrSkillFactory.create_batch(5)
        url = reverse('hr:bimahrskill-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_skill(self):
        skill = BimaHrSkillFactory()
        url = reverse('hr:bimahrskill-detail', kwargs={'pk': str(skill.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaHrSkill.objects.get(pk=skill.pk).name, 'Updated Name')

    def test_delete_skill(self):
        skill = BimaHrSkillFactory()
        url = reverse('hr:bimahrskill-detail', kwargs={'pk': str(skill.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('hr:bimahrskill-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('hr:bimahrskill-list')
        response = self.client.post(url, self.skill_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        skill = BimaHrSkillFactory()
        url = reverse('hr:bimahrskill-detail', kwargs={'pk': str(skill.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        skill = BimaHrSkillFactory()
        url = reverse('hr:bimahrskill-detail', kwargs={'pk': str(skill.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('hr.skill.can_create', 'Can create skill'),
            ('hr.skill.can_update', 'Can update skill'),
            ('hr.skill.can_delete', 'Can delete skill'),
            ('hr.skill.can_read', 'Can read skill'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaHrSkill)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
>>>>>>> origin/ma-branch
