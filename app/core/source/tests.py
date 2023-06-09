from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .factories import BimaCoreSourceFactory
from .models import BimaCoreSource
class BimaCoreSourceViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.source = BimaCoreSourceFactory.create()

    def test_create_source(self):
        url = reverse('core:bimacoresource-list')
        data = {
            "name": "my-test-source",
            "description": "my-test-description",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BimaCoreSource.objects.count(), 2)
        self.assertEqual(BimaCoreSource.objects.get(name="my-test-source").name, "my-test-source")
        self.assertEqual(response.data['name'], "my-test-source")

    def test_retrieve_source(self):
        url = reverse("core:bimacoresource-detail", kwargs={'pk': self.source.public_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.source.name)

    def test_update_source(self):
        url = reverse("core:bimacoresource-detail", kwargs={'pk': self.source.public_id})
        data = {
            "name": "my-updated-name-source",
            "description": "my-updated-code-description"
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "my-updated-name-source")
        self.assertEqual(BimaCoreSource.objects.get(name="my-updated-name-source").name, "my-updated-name-source")

    def test_delete_source(self):
        url = reverse("core:bimacoresource-detail", kwargs={"pk": self.source.public_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

