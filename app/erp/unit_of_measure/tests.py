from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .factories import BimaErpUnitOfMeasureFactory
from .models import BimaErpUnitOfMeasure
class BimaErpUnitOfMeasureViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.measure = BimaErpUnitOfMeasureFactory.create()

    def test_create_bima_erp_unit_of_measure(self):
        url = reverse('erp:bimaerpunitofmeasure-list')
        data = {
            "name": "BimaErpUnitOfMeasure_test",
            "active": True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BimaErpUnitOfMeasure.objects.count(), 2)
        self.assertEqual(BimaErpUnitOfMeasure.objects.get(name="BimaErpUnitOfMeasure_test").name, "BimaErpUnitOfMeasure_test")
        self.assertEqual(response.data['name'], "BimaErpUnitOfMeasure_test")

    def test_retrieve_bima_erp_unit_of_measure(self):
        url = reverse("erp:bimaerpunitofmeasure-detail", kwargs={'pk': self.measure.public_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.measure.name)

    def test_update_bima_erp_unit_of_measure(self):
        url = reverse("erp:bimaerpunitofmeasure-detail", kwargs={'pk': self.measure.public_id})
        data = {
            "name": "Update_BimaErpUnitOfMeasure_test",
            "active": False,

        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Update_BimaErpUnitOfMeasure_test")
        self.assertEqual(BimaErpUnitOfMeasure.objects.get(name="Update_BimaErpUnitOfMeasure_test").name, "Update_BimaErpUnitOfMeasure_test")

    def test_delete_bima_erp_unit_of_measure(self):
        url = reverse("erp:bimaerpunitofmeasure-detail", kwargs={"pk": self.measure.public_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

