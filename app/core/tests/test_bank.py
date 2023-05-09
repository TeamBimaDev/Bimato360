import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.app.settings")
django.setup()
import pytest
from django.urls import reverse
from rest_framework import status
from core.bank.models import BimaCoreBank
from core.bank.serializers import BimaCoreBankSerializer
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestBimaCoreBankViewSet:
    data = {
        'name': 'Test Bank',
        'street': '123 Test Street',
        'street2': 'street2',
        'zip': '12345',
        'city': 'Test City',
        'state': 1,
        'country': 1,
        'email': 'tests@tests.com',
        'bic': 'TEST1234'
    }
    def test_create_bank(self,):
        url_create = reverse('core:bimacorebank-list')
        client = APIClient()
        response = client.post(url_create, self.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == 'Test Bank'
        assert response.json()["street"] == '123 Test Street'
        assert response.json()["street2"] == 'street2'
        assert response.json()["zip"] == '12345'
        assert response.json()["city"] == 'Test City'
        assert response.json()["state"] == 1
        assert response.json()["country"] == 1
        assert response.json()["email"] == 'tests@tests.com'
        assert response.json()["bic"] == 'TEST1234'

    def test_retrieve_bank(self, bank):
        url_detail = reverse('core:bimacorebank-detail', args=[bank.public_id])
        client = APIClient()
        response = client.get(url_detail)
        assert response.status_code == status.HTTP_200_OK
        serializer = BimaCoreBankSerializer(bank)
        assert response.data == serializer.data

    def test_list_banks(self, bank):
        url_list = reverse('core:bimacorebank-list')
        client = APIClient()
        response = client.get(url_list)
        assert response.status_code == status.HTTP_200_OK
        serializer = BimaCoreBankSerializer([bank], many=True)
        assert response.data == serializer.data

    def test_update_bank(self, bank):
        url_update = reverse('core:bimacorebank-detail', args=[bank.public_id])
        client = APIClient()
        update_data = {
            'name': 'New Bank Name',
            'street': '123 New Street',
            'street2': 'street2',
            'zip': '67890',
            'city': 'New City',
            'state': 1,
            'country': 1,
            'email': 'new@tests.com',
            'bic': 'NEW1234'
        }
        response = client.put(url_update, update_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        bank.refresh_from_db()
        assert bank.name == 'New Bank Name'
        assert bank.street == '123 New Street'
        assert bank.street2 == 'street2'
        assert bank.zip == '67890'
        assert bank.city == 'New City'
        assert bank.email == 'new@tests.com'
        assert bank.bic == 'NEW1234'

    def test_delete_bank(self, bank):
        url_delete = reverse('core:bimacorebank-detail', args=[bank.public_id])
        client = APIClient()
        response = client.delete(url_delete)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert BimaCoreBank.objects.count() == 0
