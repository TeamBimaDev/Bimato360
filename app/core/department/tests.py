from django.test import TestCase
from django.urls import reverse

from .factories import BimaCoreDepartmentFactory
from .models import BimaCoreDepartment
from rest_framework.test import APIClient


class BimaCoreDepartmentViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.department = BimaCoreDepartmentFactory.create()
        self.child_department = BimaCoreDepartmentFactory.create(department=self.department)
        self.grandchild_department = BimaCoreDepartmentFactory.create(department=self.child_department)

    def test_create_department(self):
        url = reverse("core:bimacoredepartment-list")
        data = {
            "name": "my_new_department_name",
            "description": "my_new_department_description",
            "manager": 21,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], "my_new_department_name")
        self.assertEqual(BimaCoreDepartment.objects.count(), 4)
        self.assertEqual(BimaCoreDepartment.objects.get(name="my_new_department_name").name, "my_new_department_name")

    def test_create_department_with_sub_department(self):
        url = reverse("core:bimacoredepartment-list")
        data = {
            "name": "my_new_department_name",
            "description": "my_new_department_description",
            "manager": 21,
            "department_public_id": str(self.department.public_id)
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], "my_new_department_name")
        self.assertEqual(BimaCoreDepartment.objects.count(), 4)
        self.assertEqual(BimaCoreDepartment.objects.get(name="my_new_department_name").name, "my_new_department_name")
        self.assertEqual(
            BimaCoreDepartment.objects.get(name="my_new_department_name").department.public_id.hex,
            self.department.public_id.hex)
