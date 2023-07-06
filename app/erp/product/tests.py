from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .factories import BimaErpProductFactory
from .models import BimaErpProduct
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory

from erp.unit_of_measure.factories import BimaErpUnitOfMeasureFactory
from erp.vat.factories import BimaErpVatFactory
from erp.category.factories import BimaErpCategoryFactory


class BimaErpCategoryTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.category = BimaErpCategoryFactory.create()
        self.vat = BimaErpVatFactory.create()
        self.unit_of_measure = BimaErpUnitOfMeasureFactory.create()
        self.product_data = {
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

        # Give permissions to the user.
        permission = Permission.objects.get(codename='erp.product.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='erp.product.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='erp.product.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='erp.product.can_delete')
        self.user.user_permissions.add(permission)
        self.client.force_authenticate(self.user)

    def test_create_product(self):
        url = reverse('erp:bimaerpproduct-list')
        response = self.client.post(url, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaErpProduct.objects.count(), 1)

    def test_get_products(self):
        BimaErpProductFactory.create_batch(5)
        url = reverse('erp:bimaerpproduct-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_product(self):
        product = BimaErpProductFactory()
        url = reverse('erp:bimaerpproduct-detail', kwargs={'pk': str(product.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaErpProduct.objects.get(pk=product.pk).name, 'Updated Name')

    def test_delete_product(self):
        product = BimaErpProductFactory()
        url = reverse('erp:bimaerpproduct-detail', kwargs={'pk': str(product.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('erp:bimaerpproduct-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('erp:bimaerpproduct-list')
        response = self.client.post(url, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        product = BimaErpProductFactory()
        url = reverse('erp:bimaerpproduct-detail', kwargs={'pk': str(product.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        product = BimaErpProductFactory()
        url = reverse('erp:bimaerpproduct-detail', kwargs={'pk': str(product.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('erp.product.can_create', 'Can create product'),
            ('erp.product.can_update', 'Can update product'),
            ('erp.product.can_delete', 'Can delete product'),
            ('erp.product.can_read', 'Can read product'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaErpProduct)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )