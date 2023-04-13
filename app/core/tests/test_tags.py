from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.tags.models import BimaCoreTags
from core.tags.serializers import BimaCoreTagsserializer
from django.contrib.contenttypes.models import ContentType

class TestUnitaireTags(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tags_data = {
            'name': 'FullStack',
            'id_manager': 1,
            'parent_id': 1,
            'parent_type': ContentType.objects.filter(app_label="core", model="bimacoretags").first(),
        }
        self.tags = BimaCoreTags.objects.create(**self.tags_data)

    def test_get_all_addresses(self):
        response = self.client.get(reverse('core:bimacoretags-list'))
        tagss = BimaCoreTags.objects.all()
        serializer_data = BimaCoreTagsserializer(tagss, many=True).data
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_get_single_address(self):
        if hasattr(self, 'tags'):
            response = self.client.get(reverse('core:bimacoretags-detail', args=[self.tags.id]))
            tags = BimaCoreTags.objects.get(id=self.tags.id)
            serializer_data = BimaCoreTagsserializer(tags).data
            self.assertEqual(response.data, serializer_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_delete_address(self):
        if hasattr(self, 'tags'):
            response = self.client.delete(reverse('core:bimacoretags-detail', args=[self.tags.id]))
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

