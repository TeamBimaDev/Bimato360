from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.contact.models import BimaCoreContact
from core.contact.serializers import BimaCoreContactserializer
from django.contrib.contenttypes.models import ContentType
class TestUnitaireContact(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.contact_data = {
            'email': 'med@gmail.com',
            'fax': '3333333',
            'mobile': '4444444',
            'phone': '666666666',
            'parent_id': 1,
            'parent_type': ContentType.objects.filter(app_label="core", model="bimacorecontact").first(),
        }
        self.contact = BimaCoreContact.objects.create(**self.contact_data)

    def test_get_all_addresses(self):
        response = self.client.get(reverse('core:bimacorecontact-list'))
        contacts = BimaCoreContact.objects.all()
        serializer_data = BimaCoreContactserializer(contacts, many=True).data
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_get_single_address(self):
        if hasattr(self, 'contact'):
            response = self.client.get(reverse('core:bimacorecontact-detail', args=[self.contact.id]))
            contact = BimaCoreContact.objects.get(id=self.contact.id)
            serializer_data = BimaCoreContactserializer(contact).data
            self.assertEqual(response.data, serializer_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_delete_address(self):
        if hasattr(self, 'contact'):
            response = self.client.delete(reverse('core:bimacorecontact-detail', args=[self.contact.id]))
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

