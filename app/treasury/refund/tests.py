import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import BimaTreasuryRefund

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def model_data():
    return {
        'transaction': None,
        'amount': 33.87,
        'reason': 'zwyWztTUpO3UMCFswQqj8BBTiZ29K',
        'date': 2023-06-27,
    }

@pytest.mark.django_db
class TestBimaTreasuryRefundAPI:
    @pytest.fixture
    def model(self, model_data):
        return BimaTreasuryRefund.objects.create(**model_data)

    def test_create_model(self, api_client, model_data):
        url = reverse('BimaTreasuryRefund-list')
        response = api_client.post(url, data=model_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert BimaTreasuryRefund.objects.filter(**model_data).exists()

    def test_retrieve_model(self, api_client, model):
        url = reverse('BimaTreasuryRefund-detail', kwargs={'pk': model.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == BimaTreasuryRefundSerializer(model).data

    def test_update_model(self, api_client, model):
        url = reverse('BimaTreasuryRefund-detail', kwargs={'pk': model.id})
        updated_data = {
            # Add updated model data here
        }
        response = api_client.patch(url, data=updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        model.refresh_from_db()
        assert model == {model_name}.objects.get(id=model.id)

    def test_delete_model(self, api_client, model):
        url = reverse('BimaTreasuryRefund-detail', kwargs={'pk': model.id})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not BimaTreasuryRefund.objects.filter(id=model.id).exists()
