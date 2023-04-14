from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.contact.models import BimaCoreContact
from core.contact.serializers import BimaCoreContactserializer
from django.contrib.contenttypes.models import ContentType
class TestUnitaireContact(TestCase):
    def setUp(self):
        global contentType
        contentType = ContentType.objects.filter(app_label="core", model="bimacorecontact").first()
        self.client = APIClient()
        self.contact_data = {
            "email": "test@gmail.com",
            "fax": "4132352352355",
            "mobile": "545425255",
            "phone": "453252452",
            "parent_type": contentType.pk,
            "parent_id": 1,
        }
    def test_create_contact(self):
        url_create = reverse('core:bimacorecontact-list')
        response = self.client.post(url_create, data=self.contact_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_get_all_contact(self):
        response = self.client.get(reverse('core:bimacorecontact-list'))
        contacts = BimaCoreContact.objects.all()
        serializer_data = BimaCoreContactserializer(contacts, many=True).data
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_get_single_contact(self):
        if hasattr(self, 'contact'):
            response = self.client.get(reverse('core:bimacorecontact-detail', args=[self.contact.id]))
            contact = BimaCoreContact.objects.get(id=self.contact.id)
            serializer_data = BimaCoreContactserializer(contact).data
            self.assertEqual(response.data, serializer_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_delete_contact(self):
        if hasattr(self, 'contact'):
            response = self.client.delete(reverse('core:bimacorecontact-detail', args=[self.contact.id]))
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

