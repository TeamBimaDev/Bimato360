import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import BimaTreasuryPaymentProvider

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def model_data():
    return {
        'name': 'LWnwAjsXchHluHV2',
        'active': True,
        'credentials': {},
        'supports_tokenization': True,
        'supports_manual_capture': False,
        'supports_refunds': False,
    }

@pytest.mark.django_db
class TestBimaTreasuryPaymentProviderAPI:
    @pytest.fixture
    def model(self, model_data):
        return BimaTreasuryPaymentProvider.objects.create(**model_data)

    def test_create_model(self, api_client, model_data):
        url = reverse('BimaTreasuryPaymentProvider-list')
        response = api_client.post(url, data=model_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert BimaTreasuryPaymentProvider.objects.filter(**model_data).exists()

    def test_retrieve_model(self, api_client, model):
        url = reverse('BimaTreasuryPaymentProvider-detail', kwargs={'pk': model.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == BimaTreasuryPaymentProviderSerializer(model).data

    def test_update_model(self, api_client, model):
        url = reverse('BimaTreasuryPaymentProvider-detail', kwargs={'pk': model.id})
        updated_data = {
            # Add updated model data here
        }
        response = api_client.patch(url, data=updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        model.refresh_from_db()
        assert model == {model_name}.objects.get(id=model.id)

    def test_delete_model(self, api_client, model):
        url = reverse('BimaTreasuryPaymentProvider-detail', kwargs={'pk': model.id})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not BimaTreasuryPaymentProvider.objects.filter(id=model.id).exists()
