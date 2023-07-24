import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import BimaTreasuryTransactionPaymentMethodCardTransferDetail

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def model_data():
    return {
        'card_type': 'J3FPq6',
        'last_four_digits': 'bOrNWTdHMBq6v2Q29sHf',
        'name_on_card': 'z0Pg8wDC',
        'expiry_date': 2023-06-27,
    }

@pytest.mark.django_db
class TestBimaTreasuryTransactionPaymentMethodCardTransferDetailAPI:
    @pytest.fixture
    def model(self, model_data):
        return BimaTreasuryTransactionPaymentMethodCardTransferDetail.objects.create(**model_data)

    def test_create_model(self, api_client, model_data):
        url = reverse('BimaTreasuryTransactionPaymentMethodCardTransferDetail-list')
        response = api_client.post(url, data=model_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert BimaTreasuryTransactionPaymentMethodCardTransferDetail.objects.filter(**model_data).exists()

    def test_retrieve_model(self, api_client, model):
        url = reverse('BimaTreasuryTransactionPaymentMethodCardTransferDetail-detail', kwargs={'pk': model.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == BimaTreasuryTransactionPaymentMethodCardTransferDetailSerializer(model).data

    def test_update_model(self, api_client, model):
        url = reverse('BimaTreasuryTransactionPaymentMethodCardTransferDetail-detail', kwargs={'pk': model.id})
        updated_data = {
            # Add updated model data here
        }
        response = api_client.patch(url, data=updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        model.refresh_from_db()
        assert model == {model_name}.objects.get(id=model.id)

    def test_delete_model(self, api_client, model):
        url = reverse('BimaTreasuryTransactionPaymentMethodCardTransferDetail-detail', kwargs={'pk': model.id})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not BimaTreasuryTransactionPaymentMethodCardTransferDetail.objects.filter(id=model.id).exists()
