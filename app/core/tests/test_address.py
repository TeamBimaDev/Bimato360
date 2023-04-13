from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.address.models import BimaCoreAddress
from core.address.serializers import BimaCoreAddressSerializer
from django.contrib.contenttypes.models import ContentType

class TestUnitaireAdress(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.address_data = {
            'number': '1',
            'street': 'Rue ibn khouldoun',
            'street2': 'Rue ibn Jazzar',
            'zip': '3113',
            'city': 'Kairouan',
            'parent_id': 1,
            'parent_type': ContentType.objects.filter(app_label="core", model="bimacoreaddress").first(),
        }
        self.address = BimaCoreAddress.objects.create(**self.address_data)

    def test_get_all_addresses(self):
        response = self.client.get(reverse('core:bimacoreaddress-list'))
        addresses = BimaCoreAddress.objects.all()
        serializer_data = BimaCoreAddressSerializer(addresses, many=True).data
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_get_single_address(self):
        if hasattr(self, 'address'):
            response = self.client.get(reverse('core:bimacoreaddress-detail', args=[self.address.id]))
            address = BimaCoreAddress.objects.get(id=self.address.id)
            serializer_data = BimaCoreAddressSerializer(address).data
            self.assertEqual(response.data, serializer_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_delete_address(self):
        if hasattr(self, 'address'):
            response = self.client.delete(reverse('core:bimacoreaddress-detail', args=[self.address.id]))
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

