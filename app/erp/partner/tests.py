from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .factories import BimaErpPartnerFactory
from .models import BimaErpPartner



class BimaErpPartnerViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.partner = BimaErpPartnerFactory.create()

    def test_create_partner(self):
        url = reverse('erp:bimaerppartner-list')
        data = {
            "is_supplier": True,
            "is_customer": False,
            "partner_type": "INDIVIDUAL",
            "company_type": "GENERAL_PARTNERSHIP",
            "first_name": "John",
            "last_name": "Doe",
            "gender": "MALE",
            "social_security_number": "123456789",
            "id_number": "ABC123",
            "email": "john.doe@example.com",
            "phone": "1234567890",
            "fax": "0987654321",
            "company_name": "Example Company",
            "company_activity": "Example Activity",
            "vat_id_number": "VAT123",
            "status": "ACTIVE",
            "note": "Example note",
            "company_date_creation": "2022-01-01T00:00:00Z",
            "company_siren": "123456789",
            "company_siret": "987654321",
            "company_date_registration": "2022-01-01T00:00:00Z",
            "rcs_number": "RCS123",
            "company_date_struck_off": "2022-01-01T00:00:00Z",
            "company_ape_text": "Example APE Text",
            "company_ape_code": "APE123",
            "company_capital": "10000 USD"
        }

        response = self.client.post(url, data)
        print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BimaErpPartner.objects.count(), 2)
        self.assertEqual(BimaErpPartner.objects.get(partner_type="INDIVIDUAL").partner_type, "INDIVIDUAL")
        self.assertEqual(response.data['partner_type'], "INDIVIDUAL")

    def test_retrieve_partner(self):
        url = reverse('erp:bimaerppartner-detail', kwargs={'pk': self.partner.public_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.data['partner_type'], self.partner.partner_type)

    def test_update_partner(self):
        url = reverse('erp:bimaerppartner-detail', kwargs={'pk': self.partner.public_id})
        data = {
            "partner_type": "COMPANY",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BimaErpPartner.objects.get(public_id=self.partner.public_id).partner_type, "COMPANY")

    def test_delete_partner(self):
        url = reverse('erp:bimaerppartner-detail', kwargs={'pk': self.partner.public_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(BimaErpPartner.objects.count(), 0)

