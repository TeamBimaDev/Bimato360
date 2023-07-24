from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import BimaErpPurchaseDocument, BimaErpPurchaseDocumentProduct
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory
from erp.partner.factories import BimaErpPartnerFactory
from erp.category.factories import BimaErpCategoryFactory
from erp.product.factories import BimaErpProductFactory
from erp.product.models import BimaErpProduct
from erp.unit_of_measure.factories import BimaErpUnitOfMeasureFactory
from erp.vat.factories import BimaErpVatFactory


class BimaErpPurchaseDocumentTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.create_permissions()

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.partner = BimaErpPartnerFactory.create()
        self.purchase_document_data = {
            "number": "Document-1",
            "number_at_partner": "Document-1-partner",
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
            "purchase_document_products": [],
        }

        self.user.user_permissions.set(
            Permission.objects.filter(
                codename__in=[
                    'erp.purchase_document.can_create',
                    'erp.purchase_document.can_read',
                    'erp.purchase_document.can_update',
                    'erp.purchase_document.can_delete',
                    'erp.purchase_document.can_add_product',
                    'erp.purchase_document.can_update_product',
                    'erp.purchase_document.can_delete_product',
                    'erp.purchase_document.can_change_status',
                    'erp.purchase_document.can_rollback_status',
                    'erp.purchase_document.can_generate_document',
                    'erp.purchase_document.can_view_history',
                ]
            )
        )

        self.client.force_authenticate(self.user)

    def create_purchase_document(self):
        url = reverse('erp:bimaerppurchasedocument-list')
        response = self.client.post(url, self.purchase_document_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaErpPurchaseDocument.objects.count(), 1)

    def add_product_for_purchase_document(self):
        self.create_purchase_document()
        purchase_document = BimaErpPurchaseDocument.objects.first()
        public_id = purchase_document.public_id
        url = reverse('erp:bimaerppurchasedocument-list') + f'{public_id}/add_product/'
        category = BimaErpCategoryFactory.create()
        vat = BimaErpVatFactory.create()
        unit_of_measure = BimaErpUnitOfMeasureFactory.create()
        product = BimaErpProductFactory.create(category=category, vat=vat, unit_of_measure=unit_of_measure)
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
        self.assertEqual(BimaErpPurchaseDocumentProduct.objects.count(), 1)

    def test_create_purchase_document_type_quote(self):
        url = reverse('erp:bimaerppurchasedocument-list')
        response = self.client.post(url, self.purchase_document_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaErpPurchaseDocument.objects.count(), 1)

    def test_get_purchase_documents(self):
        self.create_purchase_document()
        url = reverse('erp:bimaerppurchasedocument-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

    def test_update_purchase_document(self):
        self.create_purchase_document()
        purchase_document = BimaErpPurchaseDocument.objects.first()
        url = reverse('erp:bimaerppurchasedocument-detail', kwargs={'pk': str(purchase_document.public_id)})
        data = {'number': 'Updated number'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaErpPurchaseDocument.objects.get(pk=purchase_document.pk).number, 'Updated number')

    def test_delete_purchase_document(self):
        self.create_purchase_document()
        purchase_document = BimaErpPurchaseDocument.objects.first()
        url = reverse('erp:bimaerppurchasedocument-detail', kwargs={'pk': str(purchase_document.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('erp:bimaerppurchasedocument-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create_purchase_document(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('erp:bimaerppurchasedocument-list')
        response = self.client.post(url, self.purchase_document_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update_purchase_document(self):
        self.create_purchase_document()
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        purchase_document = BimaErpPurchaseDocument.objects.first()
        url = reverse('erp:bimaerppurchasedocument-detail', kwargs={'pk': str(purchase_document.public_id)})
        data = {'number': 'Updated number'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete_purchase_document(self):
        self.create_purchase_document()
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        purchase_document = BimaErpPurchaseDocument.objects.first()
        url = reverse('erp:bimaerppurchasedocument-detail', kwargs={'pk': str(purchase_document.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_product_for_purchase_document(self):
        self.create_purchase_document()
        purchase_document = BimaErpPurchaseDocument.objects.first()
        public_id = purchase_document.public_id
        url = reverse('erp:bimaerppurchasedocument-list') + f'{public_id}/add_product/'
        category = BimaErpCategoryFactory.create()
        vat = BimaErpVatFactory.create()
        unit_of_measure = BimaErpUnitOfMeasureFactory.create()
        product = BimaErpProductFactory.create(category=category, vat=vat, unit_of_measure=unit_of_measure)
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
        self.assertEqual(BimaErpPurchaseDocumentProduct.objects.count(), 1)

    def test_delete_product_from_purchase_document(self):
        self.add_product_for_purchase_document()
        purchase_document = BimaErpPurchaseDocument.objects.first()
        purchase_document_public_id = purchase_document.public_id
        product = BimaErpProduct.objects.first()
        url = reverse('erp:bimaerppurchasedocument-list') + f'{purchase_document_public_id}/delete_product/'
        data = {
            "purchase_document_public_id": str(purchase_document.public_id),
            "product_public_id": str(product.public_id)
        }
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_product_from_purchase_document(self):
        self.add_product_for_purchase_document()
        purchase_document = BimaErpPurchaseDocument.objects.first()
        public_id = purchase_document.public_id
        product = BimaErpProduct.objects.first()
        url = reverse('erp:bimaerppurchasedocument-list') + f'{public_id}/update_product/'
        data = {
            "purchase_document_public_id": str(purchase_document.public_id),
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
        self.assertEqual(BimaErpPurchaseDocumentProduct.objects.get(pk=product.pk).name, 'sucre')

    def test_change_status_of_purchase_document(self):
        self.add_product_for_purchase_document()
        purchase_document = BimaErpPurchaseDocument.objects.first()
        url = reverse('erp:bimaerppurchasedocument-detail', kwargs={'pk': str(purchase_document.public_id)})
        new_status = 'CONFIRMED'
        data = {
            'status': new_status
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], new_status)
        purchase_document.refresh_from_db()
        self.assertEqual(BimaErpPurchaseDocument.objects.get(pk=purchase_document.pk).status, 'CONFIRMED')
    def test_view_history_of_purchase_document(self):
        self.create_purchase_document()
        purchase_document = BimaErpPurchaseDocument.objects.first()
        updated_data = {
            'number': 'Updated Number',
            'note': 'Updated Note',
        }
        url = reverse('erp:bimaerppurchasedocument-detail', kwargs={'pk': str(purchase_document.public_id)})
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_data = {
            'number': 'New Number',
            'note': 'New Note',
        }
        response = self.client.patch(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('erp:bimaerppurchasedocument-list') + f'{purchase_document.public_id}/get_history_diff/'
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
    def test_rollback_status_of_purchase_document(self):
        self.add_product_for_purchase_document()
        purchase_document = BimaErpPurchaseDocument.objects.first()
        url = reverse('erp:bimaerppurchasedocument-detail', kwargs={'pk': str(purchase_document.public_id)})
        data = {'status': 'CONFIRMED'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'CONFIRMED')
        data = {'status': 'DRAFT'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'DRAFT')
        purchase_document.refresh_from_db()
        self.assertEqual(purchase_document.status, 'DRAFT')
    def test_get_product_history(self):
        self.add_product_for_purchase_document()
        purchase_document = BimaErpPurchaseDocument.objects.first()
        url = reverse('erp:bimaerppurchasedocument-list') + f'{purchase_document.public_id}/get_product_history_diff/'
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

    @staticmethod
    def create_permissions():
        permission_list = [
            ('erp.purchase_document.can_create', 'Can create purchase document'),
            ('erp.purchase_document.can_update', 'Can update purchase document'),
            ('erp.purchase_document.can_delete', 'Can delete purchase document'),
            ('erp.purchase_document.can_read', 'Can read purchase document'),
            ('erp.purchase_document.can_add_product', 'Can add product to purchase document'),
            ('erp.purchase_document.can_update_product', 'Can update product in a purchase document'),
            ('erp.purchase_document.can_delete_product', 'Can delete product from purchase document'),
            ('erp.purchase_document.can_change_status', 'Can change status of purchase document'),
            ('erp.purchase_document.can_rollback_status', 'Can rollback status of purchase document'),
            ('erp.purchase_document.can_generate_document', 'Can generate document from purchase document'),
            ('erp.purchase_document.can_view_history', 'Can view history of purchase document'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaErpPurchaseDocument)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
