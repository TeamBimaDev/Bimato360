from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .factories import BimaCoreTagFactory
from .models import BimaCoreTag
class BimaCoreTagViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.tag = BimaCoreTagFactory.create()

    def test_create_tag(self):
        url = reverse('core:bimacoretag-list')
        data = {
            "name": "my-test-tag",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BimaCoreTag.objects.count(), 2)
        self.assertEqual(BimaCoreTag.objects.get(name="my-test-tag").name, "my-test-tag")
        self.assertEqual(response.data['name'], "my-test-tag")

    def test_retrieve_tag(self):
        url = reverse("core:bimacoretag-detail", kwargs={'pk': self.tag.public_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.tag.name)

    def test_update_tag(self):
        url = reverse("core:bimacoretag-detail", kwargs={'pk': self.tag.public_id})
        data = {
            "name": "my-updated-name-tag",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "my-updated-name-tag")
        self.assertEqual(BimaCoreTag.objects.get(name="my-updated-name-tag").name, "my-updated-name-tag")

    def test_delete_tag(self):
        url = reverse("core:bimacoretag-detail", kwargs={"pk": self.tag.public_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

