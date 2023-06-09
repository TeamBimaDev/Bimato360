from django.test import TestCase
from django.urls import reverse

from .factories import BimaErpCategoryFactory
from .models import BimaErpCategory
from rest_framework.test import APIClient


class BimaCoreCategoryViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.category = BimaErpCategoryFactory.create()
        self.child_category = BimaErpCategoryFactory.create(category=self.category)
        self.grandchild_category = BimaErpCategoryFactory.create(category=self.child_category)

    def test_create_category(self):
        url = reverse("erp:bimaerpcategory-list")
        data = {
            "name": "my_new_category_name",
            "description": "my_new_category_description",
            "active": True,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], "my_new_category_name")
        self.assertEqual(BimaErpCategory.objects.count(), 4)
        self.assertEqual(BimaErpCategory.objects.get(name="my_new_category_name").name, "my_new_category_name")

    def test_create_department_with_sub_category(self):
        url = reverse("erp:bimaerpcategory-list")
        data = {
            "name": "my_new_category_name",
            "description": "my_new_category_description",
            "active": False,
            "category_public_id": str(self.category.public_id)
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], "my_new_category_name")
        self.assertEqual(BimaErpCategory.objects.count(), 4)
        self.assertEqual(BimaErpCategory.objects.get(name="my_new_category_name").name, "my_new_category_name")
        self.assertEqual(
            BimaErpCategory.objects.get(name="my_new_category_name").category.public_id.hex,
            self.category.public_id.hex)
