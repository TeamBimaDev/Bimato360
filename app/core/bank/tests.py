from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .factories import BimaCoreBankFactory
from .models import BimaCoreBank
class BimaCoreBankViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.bank = BimaCoreBankFactory.create()

    def test_create_bank(self):
        url = reverse('core:bimacorebank-list')
        data = {
            "name": "bank1",
            "email": "mytestbank@gmail.com",
            "active": True,
            "bic": "2222",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BimaCoreBank.objects.count(), 2)
        self.assertEqual(BimaCoreBank.objects.get(name="bank1").name, "bank1")
        self.assertEqual(response.data['name'], "bank1")

    def test_retrieve_bank(self):
        url = reverse("core:bimacorebank-detail", kwargs={'pk': self.bank.public_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.bank.name)

    def test_update_bank(self):
        url = reverse("core:bimacorebank-detail", kwargs={'pk': self.bank.public_id})
        data = {
            "name": "bank2",
            "email": "myupdatetestbank@gmail.com",
            "active": False,
            "bic": "1111",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "bank2")
        self.assertEqual(BimaCoreBank.objects.get(name="bank2").name, "bank2")

    def test_delete_bank(self):
        url = reverse("core:bimacorebank-detail", kwargs={"pk": self.bank.public_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

