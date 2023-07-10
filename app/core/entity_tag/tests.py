from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import BimaCoreEntityTag
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user.factories import UserFactory
from core.bank.models import BimaCoreBank
from erp.partner.factories import BimaErpPartnerFactory
from erp.partner.models import BimaErpPartner
from core.tag.factories import BimaCoreTagFactory
from erp.product.factories import BimaErpProductFactory
from erp.product.models import BimaErpProduct


class BimaCoreEntityTagTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.tag = BimaCoreTagFactory.create()
        permission = Permission.objects.get(codename='core.entity_tag.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.entity_tag.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.entity_tag.can_delete')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='core.entity_tag.can_read')
        self.user.user_permissions.add(permission)

        self.entity_tag_data = {
            'tag_public_id': str(self.tag.public_id),
            'id_manager': 1,
            'order': 1,
        }
        # Give permissions to the user.
        self.client.force_authenticate(self.user)
    def test_create_entity_tag_with_partner(self):
        self.partner = BimaErpPartnerFactory()
        public_id = self.partner.public_id
        url = reverse('erp:bimaerppartner-list') + f'{public_id}/tags/'
        self.entity_tag_data['parent_type'] = ContentType.objects.get_for_model(self.partner).id
        self.entity_tag_data['parent_id'] = self.partner.id
        response = self.client.post(url, self.entity_tag_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreEntityTag.objects.count(), 1)
    def test_create_entity_tag_with_product(self):
        self.product = BimaErpProductFactory()
        public_id = self.product.public_id
        url = reverse('erp:bimaerpproduct-list') + f'{public_id}/tags/'
        self.entity_tag_data['parent_type'] = ContentType.objects.get_for_model(self.product).id
        self.entity_tag_data['parent_id'] = self.product.id
        response = self.client.post(url, self.entity_tag_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreEntityTag.objects.count(), 1)
    def test_update_entity_tag(self):
        self.test_create_entity_tag_with_partner()
        entity_tag = BimaCoreEntityTag.objects.first()
        entity_tag_data = {
            'order': 2
        }
        url = reverse('core:bimacoreentitytag-detail', kwargs={'pk': str(entity_tag.public_id)})
        response = self.client.patch(url, entity_tag_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaCoreEntityTag.objects.get(pk=entity_tag.pk).order, 2)
    def test_delete_entity_tag(self):
        self.test_create_entity_tag_with_partner()
        entity_tag = BimaCoreEntityTag.objects.first()
        url = reverse('core:bimacoreentitytag-detail', kwargs={'pk': str(entity_tag.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    def test_add_entity_tag_for_partner(self):
        BimaErpPartnerFactory.create()
        self.partner = BimaErpPartner.objects.first()
        public_id = self.partner.public_id
        url = reverse('erp:bimaerppartner-list') + f'{public_id}/tags/'
        self.entity_tag_data['parent_type'] = ContentType.objects.get_for_model(self.partner).id
        self.entity_tag_data['parent_id'] = self.partner.id
        response = self.client.post(url, self.entity_tag_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreEntityTag.objects.count(), 1)
    def test_add_entity_tag_for_product(self):
        BimaErpProductFactory.create()
        self.product = BimaErpProduct.objects.first()
        public_id = self.product.public_id
        url = reverse('erp:bimaerpproduct-list') + f'{public_id}/tags/'
        self.entity_tag_data['parent_type'] = ContentType.objects.get_for_model(self.product).id
        self.entity_tag_data['parent_id'] = self.product.id
        response = self.client.post(url, self.entity_tag_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreEntityTag.objects.count(), 1)
    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('core:bimacoreentitytag-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        self.test_create_entity_tag_with_partner()
        entity_tag = BimaCoreEntityTag.objects.first()
        address_data = {
            'order': 3
        }
        url = reverse('core:bimacoreentitytag-detail', kwargs={'pk': str(entity_tag.public_id)})
        response = self.client.patch(url, address_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        self.test_create_entity_tag_with_partner()
        entity_tag = BimaCoreEntityTag.objects.first()
        url = reverse('core:bimacoreentitytag-detail', kwargs={'pk': str(entity_tag.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('core.entity_tag.can_create', 'Can create entity tag'),
            ('core.entity_tag.can_update', 'Can update entity tag'),
            ('core.entity_tag.can_delete', 'Can delete entity tag'),
            ('core.entity_tag.can_read', 'Can read entity tag'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaCoreEntityTag)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )