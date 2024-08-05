from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory
<<<<<<< HEAD
from datetime import timedelta
from django.utils import timezone
=======
>>>>>>> origin/ma-branch

from.factories import BimaHrVacancieFactory, BimaHrOfferFactory
from.models import BimaHrOffre

class BimaHrOffreViewSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.vacancie = BimaHrVacancieFactory.create()
        self.offer_data = {
<<<<<<< HEAD
            #"title": self.vacancie.title.id,
=======
>>>>>>> origin/ma-branch
            "title": str(self.vacancie.title),
            "title_public_id":str(self.vacancie.public_id) ,
            "work_location": "become",
            "description": "entreprise IT en zarzis",
            "seniority": "JUNIOR",
            "tone": "Professional",
<<<<<<< HEAD
            "salary": "5000.00",
=======
            "salary": "50k-60k",
>>>>>>> origin/ma-branch
            "selected_hard_skills": "Python, Django",
            "selected_soft_skills": "communication, leadership",
            "inclusive_emojis": True,
            "include_desc": True,
            "inclusive_education": "Master",
            "inclusive_contact": "bima@gmail.com",
            "inclusive_location": True,
            "inclusive_experience": True,
<<<<<<< HEAD
            "activated_at": "2023-10-01",
            "stopped_at":"2024-04-01",
            "status":'Unpublished'
        }

        self.create_permissions()
    
        permission = Permission.objects.get(codename='hr.offre.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.offre.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.offre.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='hr.offre.can_delete')
        self.user.user_permissions.add(permission)
        
        self.client.force_authenticate(self.user)

    def create_permissions(self):
        # Define permissions for offer model
        permission_list = [
            ('hr.offre.can_create', 'Can create offre'),
            ('hr.offre.can_update', 'Can update offre'),
            ('hr.offre.can_delete', 'Can delete offre'),
            ('hr.offre.can_read', 'Can read offre'),
            ('hr.offre.can_generate_description', 'Can generate description'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaHrOffre)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
            
            
    def test_update_offre(self):
        # Création d'une instance d'offre à mettre à jour
        offre = BimaHrOfferFactory()
        # URL pour mettre à jour cette offre
        #url = reverse('update-offre', kwargs={'pk': offre.pk})
        url = f'/api/hr/offer/{offre.pk}/update-offre/'
        # Nouvelles données à envoyer dans la requête PUT
        new_data = {
            "title": str(self.vacancie.title),
            "title_public_id":str(self.vacancie.public_id) ,
            "work_location": "Zarizs",
            "description": "chauffage T",
            "seniority": "JUNIOR",
            "tone": "Professional",
            "salary": "8000.00",
            "selected_hard_skills": "Python, Django",
            "selected_soft_skills": "communication, leadership",
            "inclusive_emojis": True,
            "include_desc": True,
            "inclusive_education": "Master",
            "inclusive_contact": "bima@gmail.com",
            "inclusive_location": True,
            "inclusive_experience": True,
            "activated_at": "2023-10-01",
            "stopped_at":"2024-04-01",
            "status":'Unpublished'
            # Ajoutez d'autres champs que vous souhaitez mettre à jour
        }

        # Envoi de la requête PUT avec les nouvelles données
        response = self.client.put(url, new_data, format='json')
        print(response.json)
        

        # Vérification du code de statut HTTP
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Récupération de l'offre mise à jour depuis la base de données
        offre_updated = BimaHrOffre.objects.get(pk=offre.pk)
        print(offre_updated)

        # Vérification que les champs ont été mis à jour correctement
        self.assertEqual(offre_updated.work_location, new_data['work_location'])
        self.assertEqual(offre_updated.description, new_data['description'])
  

    def test_unauthorized_create(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        url = reverse('hr:bimahroffre-list')
        response = self.client.post(url, self.offer_data, format='json')
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
            
    def test_unauthenticated_access(self):
        self.client.logout()
        url = reverse('hr:bimahroffre-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        offre = BimaHrOfferFactory()
        url = reverse('hr:bimahroffre-detail', kwargs={'pk': str(offre.public_id)})
        data = {'availability_days': 10}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        offre = BimaHrOfferFactory()
        url = reverse('hr:bimahroffre-detail', kwargs={'pk': str(offre.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)    


    def test_create_offre(self):
        url = reverse('hr:bimahroffre-list')
        print(url)
        response = self.client.post(url, self.offer_data, format='json')
        print(response.content)
        if response.status_code != status.HTTP_201_CREATED:
            print("Response data:", response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaHrOffre.objects.count(), 1)
        
    
=======
        }

        self.client.force_authenticate(self.user)

    def test_create_offre(self):
        url = '/api/hr/offer/create-offre/'
        response = self.client.post(url, self.offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaHrOffre.objects.count(), 1)
>>>>>>> origin/ma-branch

    def test_get_offres(self):
        BimaHrOfferFactory.create_batch(5)
        url = f'/api/hr/offer/'
<<<<<<< HEAD
        print(url)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)
       
  
=======
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

>>>>>>> origin/ma-branch
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
<<<<<<< HEAD
        
    
    def test_status_change_on_activation_date(self):
        # Scenario where the current date is after the activation date
        past_date = timezone.localdate() - timedelta(days=1)
        offer = BimaHrOffre.objects.create(
            title=self.vacancie,
            activated_at=past_date,
            stopped_at=None,
            status='Unpublished'
        )
        offer.save()
        self.assertEqual(offer.status, 'Published', "Status should be 'Published' after activation date")

    def test_status_change_on_stopped_date(self):
        # Scenario where the current date is after the stopped date
        past_date = timezone.localdate() - timedelta(days=1)
        offer = BimaHrOffre.objects.create(
            title=self.vacancie,
            activated_at=past_date,
            stopped_at=past_date,
            status='Published'
        )
        offer.save()
        self.assertEqual(offer.status, 'Unpublished', "Status should be 'Unpublished' after stopped date")

    def test_no_change_before_activation_date(self):
        # Scenario where the current date is before the activation date
        future_date = timezone.localdate() + timedelta(days=1)
        offer = BimaHrOffre.objects.create(
            title=self.vacancie,
            activated_at=future_date,
            stopped_at=None,
            status='Unpublished'
        )
        offer.save()
        self.assertEqual(offer.status, 'Unpublished', "Status should remain 'Unpublished' before activation date")

    def test_no_change_before_stopped_date(self):
        # Scenario where the current date is before the stopped date
        future_date = timezone.localdate() + timedelta(days=1)
        offer = BimaHrOffre.objects.create(
            title=self.vacancie,
            activated_at=timezone.localdate(),
            stopped_at=future_date,
            status='Published'
        )
        offer.save()
        self.assertEqual(offer.status, 'Published', "Status should remain 'Published' before stopped date")

    def test_activated_at_conversion(self):
        # Scenario to check if activated_at conversion works properly
        past_datetime = timezone.localtime() - timedelta(days=1)
        offer = BimaHrOffre.objects.create(
            title=self.vacancie,
            activated_at=past_datetime,
            stopped_at=None,
            status='Unpublished'
        )
        offer.save()
        self.assertEqual(offer.status, 'Published', "Status should be 'Published' after activation date when activated_at is a datetime")

    def test_stopped_at_conversion(self):
        # Scenario to check if stopped_at conversion works properly
        past_datetime = timezone.localtime() - timedelta(days=1)
        offer = BimaHrOffre.objects.create(
            title=self.vacancie,
            activated_at=timezone.localdate(),
            stopped_at=past_datetime,
            status='Published'
        )
        offer.save()
        self.assertEqual(offer.status, 'Unpublished', "Status should be 'Unpublished' after stopped date when stopped_at is a datetime")




    
        
=======
>>>>>>> origin/ma-branch

