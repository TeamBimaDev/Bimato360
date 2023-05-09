from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.tags.models import BimaCoreTags
from core.tags.serializers import BimaCoreTagsserializer
from django.contrib.contenttypes.models import ContentType

class TestUnitaireTags(TestCase):
    def setUp(self):
        global contentType
        contentType = ContentType.objects.filter(app_label="core", model="bimacoretags").first()
        self.client = APIClient()
        self.tags_data = {
            'name': 'FullStack',
            'id_manager': 1,
            'parent_id': 1,
            'parent_type':contentType.pk,
        }
    def test_create_tags(self):
        url_create = reverse('core:bimacoretags-list')
        response = self.client.post(url_create, data=self.tags_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_get_all_tags(self):
        response = self.client.get(reverse('core:bimacoretags-list'))
        tagss = BimaCoreTags.objects.all()
        serializer_data = BimaCoreTagsserializer(tagss, many=True).data
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_get_single_tags(self):
        if hasattr(self, 'tags'):
            response = self.client.get(reverse('core:bimacoretags-detail', args=[self.tags.id]))
            tags = BimaCoreTags.objects.get(id=self.tags.id)
            serializer_data = BimaCoreTagsserializer(tags).data
            self.assertEqual(response.data, serializer_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_delete_tags(self):
        if hasattr(self, 'tags'):
            response = self.client.delete(reverse('core:bimacoretags-detail', args=[self.tags.id]))
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_tags(self):
        if hasattr(self, 'tags'):
            updated_tags_data = {
                'name': 'NewTag',
                'id_manager': 2,
                'parent_id': 2,
                'parent_type': contentType.pk,
            }
            response = self.client.put(reverse('core:bimacoretags-detail', args=[self.tags.id]), data=updated_tags_data, format='json')
            updated_tags = BimaCoreTags.objects.get(id=self.tags.id)
            serializer_data = BimaCoreTagsserializer(updated_tags).data
            self.assertEqual(response.data, serializer_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
