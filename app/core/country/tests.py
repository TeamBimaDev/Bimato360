from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .factories import BimaCoreCountryFactory, BimaCoreCurrencyFactory
from .models import BimaCoreCountry, BimaCoreCurrency


class BimaCoreCountryViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.currency = BimaCoreCurrencyFactory.create()
        self.country = BimaCoreCountryFactory.create(currency=self.currency)

    def test_create_country(self):
        url = reverse('core:bimacorecountry-list')  # Replace with the actual name of the URL
        data = {
            "name": "Test country",
            "code": "TC",
            "address_format": "Test address format",
            "phone_code": 1234,
            "vat_label": "VAT",
            "zip_required": True,
            "currency_public_id": str(self.currency.public_id)
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BimaCoreCountry.objects.count(), 2)
        self.assertEqual(BimaCoreCountry.objects.get(name="Test country").name, "Test country")
        self.assertEqual(response.data['name'], "Test country")

    def test_retrieve_country(self):
        url = reverse('core:bimacorecountry-detail', kwargs={'pk': self.country.public_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.country.name)

    def test_update_country(self):
        url = reverse('core:bimacorecountry-detail', kwargs={'pk': self.country.public_id})
        data = {
            "name": "Updated Test country",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BimaCoreCountry.objects.get(public_id=self.country.public_id).name, "Updated Test country")

    def test_delete_country(self):
        url = reverse('core:bimacorecountry-detail', kwargs={'pk': self.country.public_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(BimaCoreCountry.objects.count(), 0)

    def test_unique_name(self):
        url = reverse('core:bimacorecountry-list')
        data = {
            "name": self.country.name,
            "code": "TC2",
            "address_format": "Test address format",
            "phone_code": 1234,
            "vat_label": "VAT",
            "zip_required": True,
            "currency_public_id": str(self.currency.public_id)
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_unique_code(self):
        url = reverse('core:bimacorecountry-list')
        data = {
            "code": self.country.code,
            "name": "TC12",
            "address_format": "Test address format",
            "phone_code": 1234,
            "vat_label": "VAT",
            "zip_required": True,
            "currency_public_id": str(self.currency.public_id)
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
