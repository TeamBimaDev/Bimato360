from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.source.models import BimaCoreSource
from core.source.serializers import BimaCoreSourceSerializer

class TestUnitaireSource(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.source_data = {
            'name': 'linkedIn',
            'description': 'par linkedIn',
        }

    def test_get_all_sources(self):
        response = self.client.get(reverse('core:bimacoresource-list'))
        sources = BimaCoreSource.objects.all()
        serializer_data = BimaCoreSourceSerializer(sources, many=True).data
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_get_single_source(self):
        if hasattr(self, 'source'):
            response = self.client.get(reverse('core:bimacoresource-detail', args=[self.source.id]))
            source = BimaCoreSource.objects.get(id=self.source.id)
            serializer_data = BimaCoreSourceSerializer(source).data
            self.assertEqual(response.data, serializer_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_delete_source(self):
        if hasattr(self, 'source'):
            response = self.client.delete(reverse('core:bimacoresource-detail', args=[self.source.id]))
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

