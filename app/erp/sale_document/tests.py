from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import BimaErpSaleDocument, BimaErpSaleDocumentProduct
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory
from erp.partner.factories import BimaErpPartnerFactory
from erp.category.factories import BimaErpCategoryFactory
from erp.product.factories import BimaErpProductFactory
from erp.product.models import BimaErpProduct
from erp.unit_of_measure.factories import BimaErpUnitOfMeasureFactory
from erp.vat.factories import BimaErpVatFactory


class BimaErpSaleDocumentTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.create_permissions()

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.partner = BimaErpPartnerFactory.create()
        self.sale_document_data = {
            "number": "Document-1",
            "date": "2023-07-13",
            "status": "DRAFT",
            "type": "QUOTE",
            "partner_public_id": str(self.partner.public_id),
            "vat_label": "VAT",
            "vat_amount": "123.456",
            "note": "Sample note",
            "private_note": "Sample private note",
            "validity": "day_30",
            "payment_terms": "Payment terms",
            "delivery_terms": "Delivery terms",
            "total_amount_without_vat": "789.012",
            "total_after_discount": "345.678",
            "total_vat": "234.567",
            "total_amount": "901.234",
            "total_discount": "123.456",
            "is_recurring": True,
            "recurring_interval": 2,
            "sale_document_products": [],
        }

        self.user.user_permissions.set(
            Permission.objects.filter(
                codename__in=[
                    'erp.sale_document.can_create',
                    'erp.sale_document.can_read',
                    'erp.sale_document.can_update',
                    'erp.sale_document.can_delete',
                    'erp.sale_document.can_add_product',
                    'erp.sale_document.can_update_product',
                    'erp.sale_document.can_delete_product',
                    'erp.sale_document.can_change_status',
                    'erp.sale_document.can_rollback_status',
                    'erp.sale_document.can_generate_document',
                    'erp.sale_document.can_view_history',
                ]
            )
        )

        self.client.force_authenticate(self.user)

    def create_sale_document(self):
        url = reverse('erp:bimaerpsaledocument-list')
        response = self.client.post(url, self.sale_document_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaErpSaleDocument.objects.count(), 1)
    def test_create_sale_document_type_quote(self):
        url = reverse('erp:bimaerpsaledocument-list')
        response = self.client.post(url, self.sale_document_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaErpSaleDocument.objects.count(), 1)


    @staticmethod
    def create_permissions():
        permission_list = [
            ('erp.sale_document.can_create', 'Can create sale document'),
            ('erp.sale_document.can_update', 'Can update sale document'),
            ('erp.sale_document.can_delete', 'Can delete sale document'),
            ('erp.sale_document.can_read', 'Can read sale document'),
            ('erp.sale_document.can_add_product', 'Can add product to sale document'),
            ('erp.sale_document.can_update_product', 'Can update product in a sale document'),
            ('erp.sale_document.can_delete_product', 'Can delete product from sale document'),
            ('erp.sale_document.can_change_status', 'Can change status of sale document'),
            ('erp.sale_document.can_rollback_status', 'Can rollback status of sale document'),
            ('erp.sale_document.can_generate_document', 'Can generate document from sale document'),
            ('erp.sale_document.can_view_history', 'Can view history of sale document'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaErpSaleDocument)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
