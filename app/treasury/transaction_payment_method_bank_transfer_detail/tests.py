import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import BimaTreasuryTransactionPaymentMethodBankTransferDetail

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def model_data():
    return {
        'partner_bank_name': '370ibFkmS3QkH4OCtu',
        'partner_bank_name_account_number': 'gI4znlFuhX6TyXsa2gcm',
    }

@pytest.mark.django_db
class TestBimaTreasuryTransactionPaymentMethodBankTransferDetailAPI:
    @pytest.fixture
    def model(self, model_data):
        return BimaTreasuryTransactionPaymentMethodBankTransferDetail.objects.create(**model_data)

    def test_create_model(self, api_client, model_data):
        url = reverse('BimaTreasuryTransactionPaymentMethodBankTransferDetail-list')
        response = api_client.post(url, data=model_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert BimaTreasuryTransactionPaymentMethodBankTransferDetail.objects.filter(**model_data).exists()

    def test_retrieve_model(self, api_client, model):
        url = reverse('BimaTreasuryTransactionPaymentMethodBankTransferDetail-detail', kwargs={'pk': model.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == BimaTreasuryTransactionPaymentMethodBankTransferDetailSerializer(model).data

    def test_update_model(self, api_client, model):
        url = reverse('BimaTreasuryTransactionPaymentMethodBankTransferDetail-detail', kwargs={'pk': model.id})
        updated_data = {
            # Add updated model data here
        }
        response = api_client.patch(url, data=updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        model.refresh_from_db()
        assert model == {model_name}.objects.get(id=model.id)

    def test_delete_model(self, api_client, model):
        url = reverse('BimaTreasuryTransactionPaymentMethodBankTransferDetail-detail', kwargs={'pk': model.id})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not BimaTreasuryTransactionPaymentMethodBankTransferDetail.objects.filter(id=model.id).exists()
