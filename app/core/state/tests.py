from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from core.country.factories import BimaCoreCountryFactory
from .factories import BimaCoreStateFactory
from .models import BimaCoreState

class BimaCoreStateViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.country = BimaCoreCountryFactory.create()
        self.state = BimaCoreStateFactory.create(country=self.country)

    def test_create_state(self):
        url = reverse('core:bimacorestate-list')
        data = {
            "name": "my-test-state",
            "code": "my-test-code",
            "country_public_id": str(self.country.public_id)
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BimaCoreState.objects.count(), 2)
        self.assertEqual(BimaCoreState.objects.get(name="my-test-state").name, "my-test-state")
        self.assertEqual(response.data['name'], "my-test-state")

    def test_retrieve_state(self):
        url = reverse("core:bimacorestate-detail", kwargs={'pk': self.state.public_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.state.name)

    def test_update_state(self):
        url = reverse("core:bimacorestate-detail", kwargs={'pk': self.state.public_id})
        data = {
            "name": "my-updated-name-state",
            "code": "my-updated-code-state"
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "my-updated-name-state")
        self.assertEqual(BimaCoreState.objects.get(name="my-updated-name-state").name, "my-updated-name-state")

    def test_delete_state(self):
        url = reverse("core:bimacorestate-detail", kwargs={"pk": self.state.public_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

