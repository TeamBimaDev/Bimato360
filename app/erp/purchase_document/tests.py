from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .factories import BimaErpProductFactory, BimaErpPurchaseDocumentProductFactory, BimaErpPurchaseDocumentFactory
from erp.partner.factories import BimaErpPartnerFactory
from .models import BimaErpPurchaseDocument, BimaErpPurchaseDocumentProduct
from .serializers import BimaErpPurchaseDocumentProductSerializer
from decimal import Decimal

class BimaErpPurchaseDocumentViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.partner = BimaErpPartnerFactory.create()
        self.purchase_document_products = [BimaErpPurchaseDocumentProductFactory.create(),
                                       BimaErpPurchaseDocumentProductFactory.create()]
        self.purchase_document = BimaErpPurchaseDocumentFactory.create(partner=self.partner,
                                                               purchase_document_products=self.purchase_document_products)
        self.product = BimaErpProductFactory.create()

    def test_create_purchase_document(self):
        url = reverse('erp:bimaerppurchasedocument-list')

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
            "purchase_document_products": []
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BimaErpPurchaseDocument.objects.count(), 4)
        purchase_document = BimaErpPurchaseDocument.objects.get(number="DOC-2")
        self.assertEqual(purchase_document.number, "DOC-2")

    def test_retrieve_purchase_document(self):
        url = reverse('erp:bimaerppurchasedocument-detail', kwargs={'pk': self.purchase_document.public_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['number'], self.purchase_document.number)

    def test_update_purchase_document(self):
        url = reverse('erp:bimaerppurchasedocument-detail', kwargs={'pk': self.purchase_document.public_id})
        data = {
            "number": "update DOC-1",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BimaErpPurchaseDocument.objects.get(public_id=self.purchase_document.public_id).number, "update DOC-1")

    def test_delete_purchase_document(self):
        url = reverse('erp:bimaerppurchasedocument-detail', kwargs={'pk': self.purchase_document.public_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(BimaErpPurchaseDocument.objects.count(), 2)

    def test_get_product(self):
        url = reverse('erp:bimaerppurchasedocument-get-products', kwargs={'pk': self.purchase_document.public_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        products = BimaErpPurchaseDocumentProduct.objects.filter(purchase_document=self.purchase_document)
        serializer = BimaErpPurchaseDocumentProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_add_product(self):
        url = reverse('erp:bimaerppurchasedocument-add-product', kwargs={'pk': self.purchase_document.public_id})
        product = BimaErpProductFactory.create()
        data = {
            "product_public_id": str(product.public_id),
            "purchase_document_public_id": str(self.purchase_document.public_id),
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
        self.assertEqual(BimaErpPurchaseDocumentProduct.objects.count(), 7)
        product = BimaErpPurchaseDocumentProduct.objects.get(purchase_document=self.purchase_document, product=product)
        self.assertEqual(product.name, "New Product")

    def test_update_product(self):
        url = reverse('erp:bimaerppurchasedocument-update-product', kwargs={'pk': self.purchase_document.public_id})
        url_create = reverse('erp:bimaerppurchasedocument-add-product', kwargs={'pk': self.purchase_document.public_id})

        product = BimaErpProductFactory.create()
        data = {
            "purchase_document_public_id": str(self.purchase_document.public_id),
            "product_public_id": str(product.public_id),
            "name": "Updated Product",
            "reference": "Reference 5",
            "quantity": 8,
            "unit_price": 12.990,
            "vat": 5,
            "description": "Updated product description",
            "discount": 5,
        }
        response_create = self.client.post(url_create, data)

        response = self.client.put(url, data)
        print(data)
        print(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(BimaErpPurchaseDocumentProduct.objects.count(), 7)

        updated_product = BimaErpPurchaseDocumentProduct.objects.get(purchase_document=self.purchase_document, product=product)
        self.assertEqual(updated_product.name, "Updated Product")
        self.assertEqual(updated_product.quantity, 8)
        self.assertEqual(updated_product.unit_price, Decimal('12.990'))

    def test_delete_product(self):
        url = reverse('erp:bimaerppurchasedocument-delete-product', kwargs={'pk': self.purchase_document.public_id})
        product = self.purchase_document.purchase_document_products.first()
        data = {
            "purchase_document_public_id": str(self.purchase_document.public_id),
            "product_public_id": str(product.public_id),
        }
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(BimaErpPurchaseDocumentProduct.DoesNotExist):
            BimaErpPurchaseDocumentProduct.objects.get(purchase_document=self.purchase_document, product=product)
        self.assertEqual(BimaErpPurchaseDocumentProduct.objects.count(), 5)
        updated_purchase_document = BimaErpPurchaseDocument.objects.get(public_id=self.purchase_document.public_id)
        self.assertEqual(updated_purchase_document.purchase_document_products.count(), 1)
    def test_calculate_total(self):
        product = BimaErpPurchaseDocumentProductFactory.create(
            quantity=10,
            unit_price=5.99,
            vat=5,
            discount=10
        )
        product.calculate_totals()
        self.assertEqual(round(product.total_without_vat, 2), Decimal(59.90))
        self.assertEqual(round(product.discount_amount, 2), Decimal(5.99))
        self.assertEqual(round(product.total_after_discount, 2), Decimal(53.91))
        self.assertEqual(round(product.vat_amount, 2), Decimal(2.70))
        self.assertEqual(round(product.total_price, 2), Decimal(56.61))