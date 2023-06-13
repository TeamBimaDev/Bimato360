from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .factories import BimaErpProductFactory
from .models import BimaErpProduct
from erp.unit_of_measure.factories import BimaErpUnitOfMeasureFactory
from erp.category.factories import BimaErpCategoryFactory
from erp.vat.factories import BimaErpVatFactory


class BimaErpProductViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = BimaErpCategoryFactory.create()
        self.vat = BimaErpVatFactory.create()
        self.unit_of_measure = BimaErpUnitOfMeasureFactory.create()
        self.product = BimaErpProductFactory.create(category=self.category, unit_of_measure=self.unit_of_measure,
                                                    vat=self.vat)

    def test_create_product(self):
        url = reverse('erp:bimaerpproduct-list')
        data = {
            "name": "test product",
            "reference": "REF_1",
            "description": "Lorem ipsum dolor sit amet.",
            "ean13": "1234567890123",
            "type": "SERVICE_PRODUCTS",
            "purchase_price": 12.34,
            "sell_price": 56.78,
            "price_calculation_method": "MANUAL",
            "sell_percentage": 78.90,
            "category_public_id": str(self.category.public_id),
            "vat_public_id": str(self.vat.public_id),
            "unit_of_measure_public_id": str(self.unit_of_measure.public_id),
            "status": "ACTIVE",
            "minimum_stock_level": 10,
            "maximum_stock_level": 100,
            "dimension": "Dimensions",
            "weight": "Weight",
            "reorder_point": 20,
            "lead_time": 7,
            "serial_number": "Serial Number",
            "quantity": 50.0,
            "virtual_quantity": 30.0
        }

        response = self.client.post(url, data)
        print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BimaErpProduct.objects.count(), 2)
        self.assertEqual(BimaErpProduct.objects.get(name="test product").name, "test product")
        self.assertEqual(response.data['name'], "test product")

    def test_retrieve_product(self):
        url = reverse('erp:bimaerpproduct-detail', kwargs={'pk': self.product.public_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.product.name)

    def test_update_product(self):
        url = reverse('erp:bimaerpproduct-detail', kwargs={'pk': self.product.public_id})
        data = {
            "name": "update test product",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BimaErpProduct.objects.get(public_id=self.product.public_id).name, "update test product")

    def test_delete_product(self):
        url = reverse('erp:bimaerpproduct-detail', kwargs={'pk': self.product.public_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(BimaErpProduct.objects.count(), 0)
