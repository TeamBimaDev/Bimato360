import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import BimaTreasuryTransactionPaymentMethodChequeDetail

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def model_data():
    return {
        'transaction_payment_method': None,
        'bank_name': 'nmlQycKAnE',
        'cheque_number': 'cwkxRkU2ME2G3',
        'issue_date': 2023-06-27,
        'account_number': 'KZnt3vBtuB',
    }

@pytest.mark.django_db
class TestBimaTreasuryTransactionPaymentMethodChequeDetailAPI:
    @pytest.fixture
    def model(self, model_data):
        return BimaTreasuryTransactionPaymentMethodChequeDetail.objects.create(**model_data)

    def test_create_model(self, api_client, model_data):
        url = reverse('BimaTreasuryTransactionPaymentMethodChequeDetail-list')
        response = api_client.post(url, data=model_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert BimaTreasuryTransactionPaymentMethodChequeDetail.objects.filter(**model_data).exists()

    def test_retrieve_model(self, api_client, model):
        url = reverse('BimaTreasuryTransactionPaymentMethodChequeDetail-detail', kwargs={'pk': model.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == BimaTreasuryTransactionPaymentMethodChequeDetailSerializer(model).data

    def test_update_model(self, api_client, model):
        url = reverse('BimaTreasuryTransactionPaymentMethodChequeDetail-detail', kwargs={'pk': model.id})
        updated_data = {
            # Add updated model data here
        }
        response = api_client.patch(url, data=updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        model.refresh_from_db()
        assert model == {model_name}.objects.get(id=model.id)

    def test_delete_model(self, api_client, model):
        url = reverse('BimaTreasuryTransactionPaymentMethodChequeDetail-detail', kwargs={'pk': model.id})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not BimaTreasuryTransactionPaymentMethodChequeDetail.objects.filter(id=model.id).exists()
