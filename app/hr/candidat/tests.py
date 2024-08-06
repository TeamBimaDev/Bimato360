from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from core.state.factories import BimaCoreStateFactory
from core.address.factories import BimaCoreAddressFactory
from user.factories import UserFactory
from django.core.files.uploadedfile import SimpleUploadedFile

from unittest.mock import patch, MagicMock
from core.document.models import BimaCoreDocument

from.factories import BimaHrCandidatFactory
from.models import BimaHrCandidat
from hr.candidat.factories import BimaHrCandidatFactory
from core.country.factories import BimaCoreCountryFactory
from core.contact.factories import BimaCoreContactFactory
from hr.skill.factories import BimaHrSkillFactory
from hr.service import add_or_update_person_skill

class BimaHrCandidatTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.country= BimaCoreCountryFactory.create()
        self.state= BimaCoreStateFactory.create()
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
        self.file_content = "file_content".encode()


        permission = Permission.objects.get(codename='hr.candidat.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.candidat.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.candidat.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.candidat.can_delete')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.candidat.can_manage_skill')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.candidat.can_manage_experience')
        self.user.user_permissions.add(permission)
        self.client.force_authenticate(self.user)

    def create_permissions(self):
        permission_list = [
            ('hr.candidat.can_create', 'Can create candidat'),
            ('hr.candidat.can_update', 'Can update candidat'),
            ('hr.candidat.can_delete', 'Can delete candidat'),
            ('hr.candidat.can_read', 'Can read candidat'),
            ('hr.candidat.can_manage_skill', 'Can manage candidate skills'),
            ('hr.candidat.can_manage_experience','Can manage candidate experience')
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaHrCandidat)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )

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

    @patch('hr.candidat.models.BimaHrCandidat.objects.get_object_by_public_id')
    @patch('core.document.models.BimaCoreDocument.create_document_for_parent')
    def test_create_document_success(self, mock_create_document, mock_get_candidat):
        # Setup
        mock_candidat = MagicMock()
        mock_candidat.public_id = 'test-public-id'
        mock_get_candidat.return_value = mock_candidat

        mock_result = MagicMock()
        mock_result.__class__ = BimaCoreDocument
        mock_result.public_id = 'test-public-id'
        mock_result.document_name = 'test-document-name'
        mock_result.description = 'test-description'
        mock_result.date_file = '2024-07-04'
        mock_result.file_type = 'pdf'
        mock_create_document.return_value = mock_result

        # Prepare the request with a file upload
        url = reverse('hr:bimahrcandidat-list')+ f'{mock_candidat.public_id}/documents/'
        response = self.client.post(url, {
            'file_path': SimpleUploadedFile(name='test.pdf', content=self.file_content, content_type='application/pdf')
        })
        self.assertEqual(response.status_code, 201)


    @patch('hr.candidat.models.BimaHrCandidat.objects.get_object_by_public_id')
    @patch('core.document.models.BimaCoreDocument.create_document_for_parent')
    def test_create_document_failure(self, mock_create_document, mock_get_candidat):
        mock_candidat = MagicMock()
        mock_candidat.public_id = 'test-public-id'
        mock_get_candidat.return_value = mock_candidat
        mock_error_response = {'error': 'test-error'}
        mock_create_document.return_value = mock_error_response
        url = reverse('hr:bimahrcandidat-list')+ f'{mock_candidat.public_id}/documents/'
        response = self.client.post(url, {
            'file_path': SimpleUploadedFile(name='test.pdf', content=self.file_content, content_type='application/pdf')
        })
        print(response.content)
        self.assertEqual(response.status_code, 500)

    def test_create_address(self):
        candidat = BimaHrCandidatFactory.create()
        print(str(candidat.public_id))
        url = reverse('hr:bimahrcandidat-list')+ f'{candidat.public_id}' + '/addresses/'
        address_data = {
            "number": "123",
            "street": "Main St",
            "street2": "",
            "zip": "12345",
            "city": "Springfield",
            "contact_name": "John Doe",
            "contact_phone": "+1234567890",
            "contact_email": "johndoe@example.com",
            "can_send_bill": True,
            "can_deliver": True,
            "latitude": "34.0522",
            "longitude": "-118.2437",
            "note": "Test address",
            "state_public_id": str(self.state.public_id),
            "country_public_id": str(self.country.public_id)
        }
        response = self.client.post(url, address_data, format='json')
        print(response.content)  # Print the response content for debugging
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_address(self):
        candidat = BimaHrCandidatFactory()
        address = BimaCoreAddressFactory.with_parent(candidat)
        url = reverse('hr:bimahrcandidat-list')+ f'{candidat.public_id}' + '/addresses/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_contact(self):
        candidat = BimaHrCandidatFactory()
        url = reverse('hr:bimahrcandidat-list')+ f'{candidat.public_id}' + '/contacts/'
        contact_data = {
            "name": "MED",
            "position": "Manager",
            "department": "Sales",
            "email": "Med@example.com",
            "fax": "123456789",
            "mobile": "987654321",
            "phone": "555555555",
            "gender": "MALE"
        }
        response = self.client.post(url, contact_data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_contact(self):
        candidat = BimaHrCandidatFactory()
        contacts = BimaCoreContactFactory.with_parent(candidat)
        url = reverse('hr:bimahrcandidat-list')+ f'{candidat.public_id}' + '/contacts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_update_skill(self):
        candidat = BimaHrCandidatFactory()
        skill = BimaHrSkillFactory()
        url = f"/api/hr/candidat/{candidat.public_id}/add_update_skill/"
        print (url)
        skill_data = {
            "skill_public_id": skill.public_id,
            "level": 3
        }
        response = self.client.post(url, skill_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_skill(self):
        candidat = BimaHrCandidatFactory()
        skill = BimaHrSkillFactory()
        add_or_update_person_skill(candidat, skill.public_id, 3)
        url = f"/api/hr/candidat/{candidat.public_id}/delete_skill/"
        skill_data = {
            "skill_public_id": skill.public_id
        }
        response = self.client.delete(url, skill_data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_skill(self):
        candidat = BimaHrCandidatFactory()
        skill = BimaHrSkillFactory()
        add_or_update_person_skill(candidat, skill.public_id, 3)
        url = f"/api/hr/candidat/{candidat.public_id}/get_skills/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

   
  