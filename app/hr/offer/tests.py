from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory

from.factories import BimaHrVacancieFactory, BimaHrOfferFactory
from.models import BimaHrOffre

class BimaHrOffreViewSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.vacancie = BimaHrVacancieFactory.create()
        self.offer_data = {
            "title": str(self.vacancie.title),
            "title_public_id":str(self.vacancie.public_id) ,
            "work_location": "become",
            "description": "entreprise IT en zarzis",
            "seniority": "JUNIOR",
            "tone": "Professional",
            "salary": "50k-60k",
            "selected_hard_skills": "Python, Django",
            "selected_soft_skills": "communication, leadership",
            "inclusive_emojis": True,
            "include_desc": True,
            "inclusive_education": "Master",
            "inclusive_contact": "bima@gmail.com",
            "inclusive_location": True,
            "inclusive_experience": True,
        }

        self.client.force_authenticate(self.user)

    def test_create_offre(self):
        url = '/api/hr/offer/create-offre/'
        response = self.client.post(url, self.offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaHrOffre.objects.count(), 1)

    def test_get_offres(self):
        BimaHrOfferFactory.create_batch(5)
        url = f'/api/hr/offer/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # def test_update_offre(self):
    #     offer = BimaHrOfferFactory()
    #     url = f'/api/hr/offer/{offer.pk}/update-offre/'
    #     updated_data = {"description": "Updated Description"}
    #     response = self.client.put(url, updated_data, format='json')
    #     print(response.content)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(offer.description, "Updated Description")

    def test_read_offer(self):
        offer = BimaHrOfferFactory()
        url = f'/api/hr/offer/{offer.pk}/read-offre/'
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_offre(self):
        offer = BimaHrOfferFactory()
        url = f'/api/hr/offer/{offer.pk}/delete-offre/'  
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BimaHrOffre.objects.count(), 0)

    def test_generate_description(self):
        offre = BimaHrOfferFactory()
        url = f'/api/hr/offer/generate-description/{offre.pk}/' 
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(offre.generated_content)

