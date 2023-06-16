from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .factories import BimaErpProductFactory, BimaErpSaleDocumentProductFactory, BimaErpSaleDocumentFactory
from erp.partner.factories import BimaErpPartnerFactory
from .models import BimaErpSaleDocument, BimaErpSaleDocumentProduct
from .serializers import BimaErpSaleDocumentProductSerializer
from decimal import Decimal

class BimaErpSaleDocumentViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.partner = BimaErpPartnerFactory.create()
        self.sale_document_products = [BimaErpSaleDocumentProductFactory.create(),
                                       BimaErpSaleDocumentProductFactory.create()]
        self.sale_document = BimaErpSaleDocumentFactory.create(partner=self.partner,
                                                               sale_document_products=self.sale_document_products)
        self.product = BimaErpProductFactory.create()

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
        url_create = reverse('erp:bimaerpsaledocument-add-product', kwargs={'pk': self.sale_document.public_id})

        product = BimaErpProductFactory.create()
        data = {
            "sale_document_public_id": str(self.sale_document.public_id),
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
        self.assertEqual(BimaErpSaleDocumentProduct.objects.count(), 7)

        updated_product = BimaErpSaleDocumentProduct.objects.get(sale_document=self.sale_document, product=product)
        self.assertEqual(updated_product.name, "Updated Product")
        self.assertEqual(updated_product.quantity, 8)
        self.assertEqual(updated_product.unit_price, Decimal('12.990'))

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
    def test_calculate_total(self):
        product = BimaErpSaleDocumentProductFactory.create(
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