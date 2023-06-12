from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .factories import BimaErpVatFactory
from .models import BimaErpVat
class BimaErpVatViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.erpvat = BimaErpVatFactory.create()

    def test_create_bima_erp_vat(self):
        url = reverse('erp:bimaerpvat-list')
        data = {
            "name": "erpvat1",
            "rate": 2222,
            "active": True,

        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BimaErpVat.objects.count(), 2)
        self.assertEqual(BimaErpVat.objects.get(name="erpvat1").name, "erpvat1")
        self.assertEqual(response.data['name'], "erpvat1")

    def test_retrieve_bima_erp_vat(self):
        url = reverse("erp:bimaerpvat-detail", kwargs={'pk': self.erpvat.public_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.erpvat.name)

    def test_update_bima_erp_vat(self):
        url = reverse("erp:bimaerpvat-detail", kwargs={'pk': self.erpvat.public_id})
        data = {
            "name": "erpvat2",
            "rate": 1111,
            "active": False,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "erpvat2")
        self.assertEqual(BimaErpVat.objects.get(name="erpvat2").name, "erpvat2")

    def test_delete_bima_erp_vat(self):
        url = reverse("erp:bimaerpvat-detail", kwargs={"pk": self.erpvat.public_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

