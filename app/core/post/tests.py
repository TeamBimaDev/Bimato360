from django.test import TestCase
from django.urls import reverse
from core.department.factories import BimaCoreDepartmentFactory
from .factories import BimaCorePostFactory
from .models import BimaCorePost
from rest_framework.test import APIClient


class BimaCorePostViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.department = BimaCoreDepartmentFactory.create()
        self.post = BimaCorePostFactory.create(department=self.department)

    def test_create_post(self):
        url = reverse("core:bimacorepost-list")
        data = {
            "name": "my_new_post_name",
            "department_public_id": str(self.department.public_id)

        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], "my_new_post_name")
        self.assertEqual(BimaCorePost.objects.count(), 2)
        self.assertEqual(BimaCorePost.objects.get(name="my_new_post_name").name, "my_new_post_name")

    def test_retrieve_post(self):
        url = reverse("core:bimacorepost-detail", kwargs={'pk': self.post.public_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.post.name)

    def test_update_post(self):
        url = reverse("core:bimacorepost-detail", kwargs={'pk': self.post.public_id})
        data = {
            "name": "my-updated-name-post",
            "department_public_id": str(self.department.public_id)
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "my-updated-name-post")
        self.assertEqual(BimaCorePost.objects.get(name="my-updated-name-post").name, "my-updated-name-post")

    def test_delete_post(self):
        url = reverse("core:bimacorepost-detail", kwargs={"pk": self.post.public_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

