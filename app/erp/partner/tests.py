from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .factories import BimaErpPartnerFactory
from .models import BimaErpPartner



class BimaCoreCountryViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.partner = BimaErpPartnerFactory.create()

    def test_create_partner(self):
        url = reverse('erp:bimaerppartner-list')
        data = {
                "is_supplier" : True,
                "is_customer" : True,
                "partner_type" : "Individual",
                "company_type" : "Limited partnership",
                "first_name" :"ffff",
                "last_name" : "eeee",
                "gender" : "MALE",
                "social_security_number" : "fffff",
                "id_number" : "eeeeee",
                "email" : "email@gmail.com",
                "phone" : "22323",
                "fax" : "ddddd",
                "company_name" :"rerere",
                "company_activity" : "efeere",
                "vat_id_number" : "rerere",
                "status" : "Active",
                "note" : "",
                "company_date_creation" : "",
                "company_siren" : "",
                "company_siret" : "",
                "company_date_registration" : "",
                "rcs_number" : "",
                "company_date_struck_off" : "",
                "company_ape_text" : "",
                "company_ape_code" : "",
                "company_capital" : "",

        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BimaErpPartner.objects.count(), 2)
        self.assertEqual(BimaErpPartner.objects.get(name="Test country").name, "Test country")
        self.assertEqual(response.data['name'], "Test country")

    def test_retrieve_partner(self):
        url = reverse('erp:bimaerppartner-detail', kwargs={'pk': self.partner.public_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.partner.name)

    def test_update_partner(self):
        url = reverse('erp:bimaerppartner-detail', kwargs={'pk': self.partner.public_id})
        data = {
            "name": "Updated Test country",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BimaErpPartner.objects.get(public_id=self.partner.public_id).name, "Updated Test country")

    def test_delete_partner(self):
        url = reverse('erp:bimaerppartner-detail', kwargs={'pk': self.partner.public_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(BimaErpPartner.objects.count(), 0)

