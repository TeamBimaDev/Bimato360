import itertools

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from erp.category.factories import BimaErpCategoryFactory
from erp.partner.factories import BimaErpPartnerFactory
from erp.product.factories import BimaErpProductFactory
from erp.product.models import BimaErpProduct
from erp.unit_of_measure.factories import BimaErpUnitOfMeasureFactory
from erp.vat.factories import BimaErpVatFactory
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory

from .models import BimaErpSaleDocument, BimaErpSaleDocumentProduct


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
            "type": "INVOICE",
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
            "recurring_interval": "DAILY",
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

        self.document_number_counter = itertools.count(start=1)

    def create_sale_document(self):
        url = reverse('erp:bimaerpsaledocument-list')
        document_number = f"Document-{next(self.document_number_counter)}"
        self.sale_document_data['number'] = document_number
        response = self.client.post(url, self.sale_document_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def add_product_for_sale_document(self):
        self.create_sale_document()
        sale_document = BimaErpSaleDocument.objects.first()
        public_id = sale_document.public_id
        url = reverse('erp:bimaerpsaledocument-list') + f'{public_id}/add_product/'
        category = BimaErpCategoryFactory.create()
        vat = BimaErpVatFactory.create()
        unit_of_measure = BimaErpUnitOfMeasureFactory.create()
        product = BimaErpProductFactory.create(category=category, vat=vat, unit_of_measure=unit_of_measure,
                                               quantity=0, type="SERVICE_PRODUCTS")
        data = {
            "unit_of_measure": "Kilo",
            "vat": 12,
            "unit_price": 1200,
            "discount": 0,
            "quantity": 3,
            "reference": "2313241564",
            "name": "Sale",
            "product_public_id": str(product.public_id),
            "description": ""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaErpSaleDocumentProduct.objects.count(), 1)

    def test_create_sale_document_type_quote(self):
        url = reverse('erp:bimaerpsaledocument-list')
        response = self.client.post(url, self.sale_document_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaErpSaleDocument.objects.count(), 1)

    def test_get_sale_documents(self):
        self.create_sale_document()
        url = reverse('erp:bimaerpsaledocument-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

    def test_update_sale_document(self):
        self.create_sale_document()
        sale_document = BimaErpSaleDocument.objects.first()
        url = reverse('erp:bimaerpsaledocument-detail', kwargs={'pk': str(sale_document.public_id)})
        data = {'number': 'Updated number'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaErpSaleDocument.objects.get(pk=sale_document.pk).number, 'Updated number')

    def test_delete_sale_document(self):
        self.create_sale_document()
        sale_document = BimaErpSaleDocument.objects.first()
        url = reverse('erp:bimaerpsaledocument-detail', kwargs={'pk': str(sale_document.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('erp:bimaerpsaledocument-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create_sale_document(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('erp:bimaerpsaledocument-list')
        response = self.client.post(url, self.sale_document_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update_sale_document(self):
        self.create_sale_document()
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        sale_document = BimaErpSaleDocument.objects.first()
        url = reverse('erp:bimaerpsaledocument-detail', kwargs={'pk': str(sale_document.public_id)})
        data = {'number': 'Updated number'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete_sale_document(self):
        self.create_sale_document()
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        sale_document = BimaErpSaleDocument.objects.first()
        url = reverse('erp:bimaerpsaledocument-detail', kwargs={'pk': str(sale_document.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_product_for_sale_document(self):
        self.create_sale_document()
        sale_document = BimaErpSaleDocument.objects.first()
        public_id = sale_document.public_id
        url = reverse('erp:bimaerpsaledocument-list') + f'{public_id}/add_product/'
        category = BimaErpCategoryFactory.create()
        vat = BimaErpVatFactory.create()
        unit_of_measure = BimaErpUnitOfMeasureFactory.create()
        product = BimaErpProductFactory.create(category=category, vat=vat, unit_of_measure=unit_of_measure, quantity=1,
                                               type="STOCKABLE_PRODUCT")
        data = {
            "unit_of_measure": "Kilo",
            "vat": 12,
            "unit_price": 1200,
            "discount": 0,
            "quantity": 3,
            "reference": "2313241564cqqsqsqsqs",
            "name": "Sale2",
            "product_public_id": str(product.public_id),
            "description": "sqdqsdzaeazezae"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaErpSaleDocumentProduct.objects.count(), 1)

    def test_delete_product_from_sale_document(self):
        self.add_product_for_sale_document()
        sale_document = BimaErpSaleDocument.objects.first()
        sale_document_public_id = sale_document.public_id
        product = BimaErpProduct.objects.first()
        url = reverse('erp:bimaerpsaledocument-list') + f'{sale_document_public_id}/delete_product/'
        data = {
            "sale_document_public_id": str(sale_document.public_id),
            "product_public_id": str(product.public_id)
        }
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_product_from_sale_document(self):
        self.add_product_for_sale_document()
        sale_document = BimaErpSaleDocument.objects.first()
        public_id = sale_document.public_id
        product = BimaErpProduct.objects.first()
        url = reverse('erp:bimaerpsaledocument-list') + f'{public_id}/update_product/'
        data = {
            "sale_document_public_id": str(sale_document.public_id),
            "product_public_id": str(product.public_id),
            "unit_of_measure": "Kilo",
            "vat": 12,
            "unit_price": 1200,
            "discount": 0,
            "quantity": 3,
            "reference": "2313241564",
            "name": "sucre",
            "description": ""
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaErpSaleDocumentProduct.objects.get(pk=product.pk).name, 'sucre')

    def test_change_status_of_sale_document(self):
        self.add_product_for_sale_document()
        sale_document = BimaErpSaleDocument.objects.first()
        url = reverse('erp:bimaerpsaledocument-detail', kwargs={'pk': str(sale_document.public_id)})
        new_status = 'CONFIRMED'
        data = {
            'status': new_status
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], new_status)
        sale_document.refresh_from_db()
        self.assertEqual(BimaErpSaleDocument.objects.get(pk=sale_document.pk).status, 'CONFIRMED')

    def test_view_history_of_sale_document(self):
        self.create_sale_document()
        sale_document = BimaErpSaleDocument.objects.first()
        updated_data = {
            'number': 'Updated Number',
            'note': 'Updated Note',
        }
        url = reverse('erp:bimaerpsaledocument-detail', kwargs={'pk': str(sale_document.public_id)})
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_data = {
            'number': 'New Number',
            'note': 'New Note',
        }
        response = self.client.patch(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('erp:bimaerpsaledocument-list') + f'{sale_document.public_id}/get_history_diff/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('differences', response.data)
        differences = response.data['differences']
        self.assertIsInstance(differences, list)
        for difference in differences:
            self.assertIsInstance(difference, dict)
            self.assertIn('date', difference)
            self.assertIn('changes', difference)
            changes = difference['changes']
            self.assertIsInstance(changes, list)
            for change in changes:
                self.assertIsInstance(change, dict)
                self.assertIn('field', change)
                self.assertIn('old_value', change)
                self.assertIn('new_value', change)
                self.assertIn('user', change)

    def test_rollback_status_of_sale_document(self):
        self.add_product_for_sale_document()
        sale_document = BimaErpSaleDocument.objects.first()
        url = reverse('erp:bimaerpsaledocument-detail', kwargs={'pk': str(sale_document.public_id)})
        data = {'status': 'CONFIRMED'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'CONFIRMED')
        data = {'status': 'DRAFT'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'DRAFT')
        sale_document.refresh_from_db()
        self.assertEqual(sale_document.status, 'DRAFT')

    def test_get_product_history(self):
        self.add_product_for_sale_document()
        sale_document = BimaErpSaleDocument.objects.first()
        url = reverse('erp:bimaerpsaledocument-list') + f'{sale_document.public_id}/get_product_history_diff/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('products_differences', response.data)
        products_differences = response.data['products_differences']
        self.assertIsInstance(products_differences, list)
        for product_difference in products_differences:
            self.assertIsInstance(product_difference, dict)
            self.assertIn('product_id', product_difference)
            self.assertIn('product_name', product_difference)
            self.assertIn('differences', product_difference)
            differences = product_difference['differences']
            self.assertIsInstance(differences, list)
            for difference in differences:
                self.assertIsInstance(difference, dict)
                self.assertIn('date', difference)
                self.assertIn('changes', difference)
                changes = difference['changes']
                self.assertIsInstance(changes, list)
                for change in changes:
                    self.assertIsInstance(change, dict)
                    self.assertIn('field', change)
                    self.assertIn('old_value', change)
                    self.assertIn('new_value', change)
                    self.assertIn('history_type', change)
                    self.assertIn('user', change)

    def test_verifies_quantity_of_product(self):
        self.create_sale_document()
        product = BimaErpProductFactory.create(quantity=100, type="STOCKABLE_PRODUCT")
        sale_document = BimaErpSaleDocument.objects.first()

        save_bima_erp_sale_document_product_url = reverse(
            'erp:bimaerpsaledocument-list') + f'{sale_document.public_id}/add_product/'
        save_bima_erp_sale_document_product_data = {
            "unit_of_measure": "Kilo",
            "vat": 12,
            "unit_price": 1200,
            "discount": 0,
            "quantity": 30,
            "reference": "2313241564cqqsqsqsqs",
            "name": "Sale2",
            "product_public_id": str(product.public_id),
            "description": "sqdqsdzaeazezae"
        }
        save_bima_erp_sale_document_product_response = self.client.post(save_bima_erp_sale_document_product_url,
                                                                        save_bima_erp_sale_document_product_data,
                                                                        format='json')
        self.assertEqual(save_bima_erp_sale_document_product_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaErpSaleDocumentProduct.objects.count(), 1)

        save_bima_erp_sale_document_url = reverse('erp:bimaerpsaledocument-detail',
                                                  kwargs={'pk': str(sale_document.public_id)})
        data = {'status': 'CONFIRMED'}
        response = self.client.patch(save_bima_erp_sale_document_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        product.refresh_from_db()
        print(product.quantity)
        self.assertEqual(product.quantity, 70)

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
