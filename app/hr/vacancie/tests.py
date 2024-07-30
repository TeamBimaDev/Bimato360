from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from.models import BimaHrVacancie, BimaHrCandidatVacancie
from.views import BimaHrVacancieViewSet
from .factories import BimaHrVacancieFactory, BimaHrCandidatVacancieFactory
from user.factories import UserFactory
from core.department.factories import BimaCoreDepartmentFactory
from hr.job_category.factories import BimaHrJobCategoryFactory
from hr.employee.factories import BimaHrEmployeeFactory
from hr.candidat.factories import BimaHrCandidatFactory


# Assuming you have a factory for creating instances of BimaHrVacancie and BimaHrCandidatVacancie

class BimaHrVacancieViewSetTests(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.departement = BimaCoreDepartmentFactory.create()
        self.job_category = BimaHrJobCategoryFactory.create()
        self.manager = BimaHrEmployeeFactory.create()
        self.vacancie_data = {
            "title": "Software Engineer",
            "description": "We are looking for a software engineer...",
            "work_location": "Remote",
            "seniority": "JUNIOR",
            "department_public_id": str(self.departement.public_id),  
            "job_category_public_id": str(self.job_category.public_id),  
            "work_mode": "ONSITE",
            "job_type": "FULL_TIME",
            "manager": str(self.manager.public_id), 
            "date_expiration": "2024-12-31",
            "date_start_vacancie": "2024-07-01",
            "number_of_positions": 1,
            "published_date": "2024-06-28T00:00:00Z",
            "position_status": "ACTIVE",
        }

        # Assign permissions to the test user
        permission = Permission.objects.get(codename='hr.vacancie.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.vacancie.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.vacancie.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.vacancie.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def create_permissions(self):
        # Define permissions for Vacancie model
        permission_list = [
            ('hr.vacancie.can_create', 'Can create vacancie'),
            ('hr.vacancie.can_update', 'Can update vacancie'),
            ('hr.vacancie.can_delete', 'Can delete vacancie'),
            ('hr.vacancie.can_read', 'Can read vacancie'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaHrVacancie)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )

    def test_create_vacancie(self):
        url = '/api/hr/vacancie/'
        response = self.client.post(url, self.vacancie_data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaHrVacancie.objects.count(), 1)

    def test_get_vacancies(self):
        BimaHrVacancieFactory.create_batch(5)
        url = '/api/hr/vacancie/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_vacancie(self):
        vacancie = BimaHrVacancieFactory()
        url = f'/api/hr/vacancie/{vacancie.public_id}/'
        data = {'title': 'Senior Software Engineer'}
        response = self.client.patch(url, data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaHrVacancie.objects.get(pk=vacancie.pk).title, 'Senior Software Engineer')

    def test_delete_vacancie(self):
        vacancie = BimaHrVacancieFactory()
        url = f'/api/hr/vacancie/{vacancie.public_id}/'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_access(self):
        self.client.logout()
        url = '/api/hr/vacancie/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        url = '/api/hr/vacancie/'
        response = self.client.post(url, self.vacancie_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        vacancie = BimaHrVacancieFactory()
        url = f'/api/hr/vacancie/{vacancie.public_id}/'
        data = {'title': 'Senior Developer'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        vacancie = BimaHrVacancieFactory()
        url = f'/api/hr/vacancie/{vacancie.public_id}/'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_candidate_application(self):
        vacancie = BimaHrVacancieFactory.create()
        candidat_vacancie = BimaHrCandidatVacancieFactory.create(vacancie=vacancie)
        url = f'/api/hr/vacancie/{vacancie.public_id}/candidat_applied/'
        response = self.client.get(url,format="json")
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_candidat(self):
        vacancie = BimaHrVacancieFactory.create()
        candidat = BimaHrCandidatFactory.create()
        data_document= {
            "file_path":"C:/Users/houssem/Desktop/projet/bima_work/bima360/back/app/media/uploads/documents/bimahrcandidat/",
            "document_name":"d14df484-2646-4c3e-9eae-a8a959456e05.jpg",
            "description":"",
            "file_type":"CANDIDAT_CV"
        }
        data = {"candidat_public_id": candidat.public_id,
                "expected_salary": 300,
                "proposed_salary": 45000,
                "accepted_salary": 48000,
                "comments": "Looking forward to this opportunity."
                }
        url= f'/api/hr/vacancie/{vacancie.public_id}/add_candidat/'
        response = self.client.post(url, data, format="json")
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_candidate_application(self):
        vacancy = BimaHrVacancieFactory.create()
        candidat_vacancie = BimaHrCandidatVacancieFactory.create(vacancie=vacancy)
        response = self.client.delete(reverse('bimahrvacancie-delete-candidat', kwargs={'candidat_vacancie_public_id': candidat_vacancie.public_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
