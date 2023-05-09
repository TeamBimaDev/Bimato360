from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.adress.models import BimaCoreAdress
from core.adress.serializers import BimaCoreAdressserializer
from django.contrib.contenttypes.models import ContentType


class TestUnitaireAdress(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.adress_data = {
            'number': '1',
            'street': 'Rue ibn khouldoun',
            'postal_code': '3113',
            'city': 'Kairouan',
            'parent_id':1,
            'parent_type': ContentType.objects.get_for_model(BimaCoreAdress),
        }
        self.adress = BimaCoreAdress.objects.create(**self.adress_data)

    def test_get_all_adresses(self):
        response = self.client.get(reverse('core:bimacoreadress-list'))
        adresses = BimaCoreAdress.objects.all()
        serializer_data = BimaCoreAdressserializer(adresses, many=True).data
        self.assertEqual(response.data, serializer_data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_create_adress(self):
        response = self.client.post(reverse('core:bimacoreadress-list'), self.adress_data)
        if response.status_code == status.HTTP_400_BAD_REQUEST:
             self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_single_adress(self):
        response = self.client.get(reverse('core:bimacoreadress-detail', args=[self.adress.id]))
        adress = BimaCoreAdress.objects.get(id=self.adress.id)
        serializer_data = BimaCoreAdressserializer(adress).data
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_adress(self):
        new_adress_data = {
            'number': '2',
            'street': 'Rue Ibn Jazzar',
            'postal_code': '4024',
            'city': 'Sousse',
            'parent_id': 2,
            'parent_type': ContentType.objects.get_for_model(BimaCoreAdress),
        }
        response = self.client.put(reverse('core:bimacoreadress-detail', args=[self.adress.id]), new_adress_data)
        for field in ['created', 'updated', 'public_id']:
            if field in response:
                del response[field]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.adress.refresh_from_db()
        self.assertEqual(self.adress.number, new_adress_data['number'])
        self.assertEqual(self.adress.street, new_adress_data['street'])
        self.assertEqual(self.adress.postal_code, new_adress_data['postal_code'])
        self.assertEqual(self.adress.city, new_adress_data['city'])
        self.assertEqual(self.adress.parent_id, new_adress_data['parent_id'])
        self.assertEqual(self.adress.parent_type, new_adress_data['parent_type'])

    def test_delete_adress(self):
        response = self.client.delete(reverse('core:bimacoreadress-detail', args=[self.adress.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BimaCoreAdress.objects.filter(id=self.adress.id).exists())
