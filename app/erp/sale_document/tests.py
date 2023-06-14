from unittest.mock import MagicMock
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .factories import BimaErpProductFactory, BimaErpSaleDocumentProductFactory, BimaErpSaleDocumentFactory
from erp.partner.factories import BimaErpPartnerFactory
from .models import BimaErpSaleDocument, BimaErpSaleDocumentProduct
from .serializers import BimaErpSaleDocumentProductSerializer
from common.service.purchase_sale_service import generate_unique_number
from datetime import datetime
from common.enums.sale_document_enum import SaleDocumentStatus

from .views import BimaErpSaleDocumentViewSet


class BimaErpSaleDocumentViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.partner = BimaErpPartnerFactory.create()
        self.sale_document_products = [BimaErpSaleDocumentProductFactory.create(),
                                       BimaErpSaleDocumentProductFactory.create()]
        self.sale_document = BimaErpSaleDocumentFactory.create(partner=self.partner, sale_document_products=self.sale_document_products)

    def test_create_sale_document(self):
        url = reverse('erp:bimaerpsaledocument-list')

        data = {
            "number": "DOC-2",
            "date": "2023-06-10",
            "status": "CONFIRMED",
            "type": "QUOTE",
            "partner_public_id": str(self.partner.public_id),
            "note": "Ceci est une note",
            "private_note": "Ceci est une note privée",
            "validity": "day_30",
            "payment_terms": "Payment Terms",
            "delivery_terms": "Delivery Terms",
            "sale_document_products": []
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BimaErpSaleDocument.objects.count(), 4)
        sale_document = BimaErpSaleDocument.objects.get(number="DOC-2")
        self.assertEqual(sale_document.number, "DOC-2")

    def test_retrieve_sale_document(self):
        url = reverse('erp:bimaerpsaledocument-detail', kwargs={'pk': self.sale_document.public_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['number'], self.sale_document.number)

    def test_update_sale_document(self):
        url = reverse('erp:bimaerpsaledocument-detail', kwargs={'pk': self.sale_document.public_id})
        data = {
            "number": "update DOC-1",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BimaErpSaleDocument.objects.get(public_id=self.sale_document.public_id).number, "update DOC-1")

    def test_delete_sale_document(self):
        url = reverse('erp:bimaerpsaledocument-detail', kwargs={'pk': self.sale_document.public_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(BimaErpSaleDocument.objects.count(), 2)
    def test_get_product(self):
        url = reverse('erp:bimaerpsaledocument-get-products', kwargs={'pk': self.sale_document.public_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        products = BimaErpSaleDocumentProduct.objects.filter(sale_document=self.sale_document)
        serializer = BimaErpSaleDocumentProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
    def test_add_product(self):
        url = reverse('erp:bimaerpsaledocument-add-product', kwargs={'pk': self.sale_document.public_id})
        product = BimaErpProductFactory.create()
        data = {
            "product_public_id": str(product.public_id),
            "sale_document_public_id": str(self.sale_document.public_id),
            "name": "New Product",
            "reference": "Reference 2",
            "quantity": 5,
            "unit_price": 9.99,
            "vat": 5,
            "description": "New product description",
            "discount": 4,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BimaErpSaleDocumentProduct.objects.count(), 7)
        product = BimaErpSaleDocumentProduct.objects.get(sale_document=self.sale_document, product=product)
        self.assertEqual(product.name, "New Product")

    def test_update_product(self):
        url = reverse('erp:bimaerpsaledocument-update-product', kwargs={'pk': self.sale_document.public_id})
        product = self.sale_document.sale_document_products.first()
        data = {
            "sale_document_public_id": str(self.sale_document.public_id),
            "product_public_id": str(product.public_id),
            "name": "Updated Product",
            "reference": "Reference 5",
            "quantity": 8,
            "unit_price": 12.99,
            "vat": 5,
            "description": "Updated product description",
            "discount": 5,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BimaErpSaleDocumentProduct.objects.count(), 6)
        try:
            updated_product = BimaErpSaleDocumentProduct.objects.get(sale_document=self.sale_document, product=product)
            self.assertEqual(updated_product.name, "Updated Product")
            self.assertEqual(updated_product.quantity, 8)
            self.assertEqual(updated_product.unit_price, 12.99)
        except BimaErpSaleDocumentProduct.DoesNotExist:
            self.fail("The updated product does not exist.")
        updated_sale_document = BimaErpSaleDocument.objects.get(public_id=self.sale_document.public_id)
        self.assertEqual(updated_sale_document.sale_document_products.count(), 2)
        self.assertEqual(updated_sale_document.sale_document_products.first().name, "Updated Product")
        self.assertEqual(len(response.data['sale_document_products']), 2)
        self.assertEqual(response.data['sale_document_products'][0]['name'], "Updated Product")

    def test_delete_product(self):
        url = reverse('erp:bimaerpsaledocument-delete-product', kwargs={'pk': self.sale_document.public_id})
        product = self.sale_document.sale_document_products.first()
        data = {
            "sale_document_public_id": str(self.sale_document.public_id),
            "product_public_id": str(product.public_id),
        }
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(BimaErpSaleDocumentProduct.DoesNotExist):
            BimaErpSaleDocumentProduct.objects.get(sale_document=self.sale_document, product=product)
        self.assertEqual(BimaErpSaleDocumentProduct.objects.count(), 5)
        updated_sale_document = BimaErpSaleDocument.objects.get(public_id=self.sale_document.public_id)
        self.assertEqual(updated_sale_document.sale_document_products.count(), 1)
    def test_calculate_totals(self):
        instance = BimaErpSaleDocumentProduct()
        instance.quantity = 10
        instance.unit_price = 100
        instance.discount = 20
        instance.vat = 10
        instance.calculate_totals()
        assert instance.total_without_vat == 1000
        assert instance.discount_amount == 200
        assert instance.total_after_discount == 800
        assert instance.vat_amount == 80
        assert instance.total_price == 880
