from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .factories import BimaErpProductFactory, BimaErpSaleDocumentProductFactory, BimaErpSaleDocumentFactory
from erp.partner.factories import BimaErpPartnerFactory
from .models import BimaErpSaleDocument


class BimaErpSaleDocumentViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.partner = BimaErpPartnerFactory.create()
        self.sale_document_product = BimaErpSaleDocumentProductFactory.create()
        self.sale_document = BimaErpSaleDocumentFactory.create(partner=self.partner, sale_document_product=self.sale_document_product)

    def test_create_sale_document(self):
        url = reverse('erp:bimaerpsaledocument-list')
        data = {
              "number": "DOC-1",
              "date": "2023-06-10",
              "status": "Confirmed",
              "type": "Quote",
              "partner_public_id": str(self.partner.public_id),
              "note": "Ceci est une note",
              "private_note": "Ceci est une note privée",
              "validity": "30 days",
              "payment_terms": "Payment Terms",
              "delivery_terms": "Delivery Terms",
              "subtotal": 123.45,
              "taxes": 12.34,
              "discounts": 5.67,
              "total": 130.12,
            }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BimaErpSaleDocument.objects.count(), 2)
        self.assertEqual(BimaErpSaleDocument.objects.get(number="DOC-1").number, "DOC-1")
        self.assertEqual(response.data['number'], "DOC-1")

    def test_retrieve_sale_document(self):
        url = reverse('erp:bimaerpsaledocument-detail', kwargs={'pk': self.sale_document.public_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['number'], self.sale_document.numbers)

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
        self.assertEqual(BimaErpSaleDocument.objects.count(), 0)
