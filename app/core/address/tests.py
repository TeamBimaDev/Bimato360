from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .factories import BimaCoreAddressFactory
from .models import BimaCoreAddress
from core.state.factories import BimaCoreStateFactory
from core.country.factories import BimaCoreCountryFactory
from django.contrib.contenttypes.models import ContentType


class BimaCoreAddressViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.state = BimaCoreStateFactory.create()
        self.country = BimaCoreCountryFactory.create()
        self.address = BimaCoreAddressFactory.create(state=self.state, country=self.country)

    def test_create_address(self):
        url = reverse('core:bimacoreaddress-list')
        data = {
            "number": "Test address",
            "street": "test_street",
            "street2": "Test_street2",
            "zip": "1234",
            "city": "test_city",
            "contact_name": True,
            "contact_email": "contactemail@gmail.com",
            "can_send_bill": "test_can_send_bill",
            "can_deliver": True,
            "latitude": True,
            "longitude": "test_longitude",
            "note": "test_note",
            "parent_id": 1,
            "parent_type": ContentType.objects.get,
            "country": str(self.country.public_id),
            "state": str(self.state.public_id)
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BimaCoreAddress.objects.count(), 2)
        self.assertEqual(BimaCoreAddress.objects.get(number="Test address").number, "Test address")
        self.assertEqual(response.data['number'], "Test address")

    def test_retrieve_address(self):
        url = reverse('core:bimacoreaddress-detail', kwargs={'pk': self.address.public_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['number'], self.address.number)

    def test_update_address(self):
        url = reverse('core:bimacoreaddress-detail', kwargs={'pk': self.address.public_id})
        data = {
            "number": "Updated Test address",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BimaCoreAddress.objects.get(public_id=self.address.public_id).name, "Updated Test address")

    def test_delete_address(self):
        url = reverse('core:bimacoreaddress-detail', kwargs={'pk': self.address.public_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(BimaCoreAddress.objects.count(), 0)
