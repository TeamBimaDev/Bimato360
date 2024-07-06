from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory
from .factories import BimaTreasuryPaymentTermFactory
from .models import BimaTreasuryPaymentTerm


class BimaTreasuryPaymentTermTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()

        self.payment_term_data = {
            'name': 'Test_payment_term',
            'active': True,
            'type': 'IMMEDIATE',
            'note': 'note payment_term',
            'code': '124578',
            'is_system': True,
        }

        # Give permissions to the user.
        permission = Permission.objects.get(codename='treasury.payment_term.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.payment_term.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.payment_term.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.payment_term.can_delete')
        self.user.user_permissions.add(permission)

        self.client.force_authenticate(self.user)

    def test_create_payment_method(self):
        url = reverse('treasury:bimatreasurypaymentterm-list')
        response = self.client.post(url, self.payment_term_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryPaymentTerm.objects.count(), 1)

    def test_custom_payment_term_percentage_sum(self):
        custom_payment_term = BimaTreasuryPaymentTermFactory(type='CUSTOM')
        custom_payment_term.check_percentage_sum()
        total_percentage = sum(detail.percentage for detail in custom_payment_term.payment_term_details.all())
        self.assertEqual(total_percentage, 100)

    def test_get_payment_methods(self):
        BimaTreasuryPaymentTermFactory.create_batch(5)
        url = reverse('treasury:bimatreasurypaymentterm-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 5)

    def test_update_payment_method(self):
        payment_term = BimaTreasuryPaymentTermFactory()
        url = reverse('treasury:bimatreasurypaymentterm-detail', kwargs={'pk': str(payment_term.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaTreasuryPaymentTerm.objects.get(pk=payment_term.pk).name, 'Updated Name')

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('treasury:bimatreasurypaymentterm-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('treasury:bimatreasurypaymentterm-list')
        response = self.client.post(url, self.payment_term_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        payment_term = BimaTreasuryPaymentTermFactory()
        url = reverse('treasury:bimatreasurypaymentterm-detail', kwargs={'pk': str(payment_term.public_id)})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        payment_term = BimaTreasuryPaymentTermFactory()
        url = reverse('treasury:bimatreasurypaymentterm-detail', kwargs={'pk': str(payment_term.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_permissions(self):
        permission_list = [
            ('treasury.payment_term.can_create', 'Can create payment term'),
            ('treasury.payment_term.can_update', 'Can update payment term'),
            ('treasury.payment_term.can_delete', 'Can delete payment term'),
            ('treasury.payment_term.can_read', 'Can read payment term'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaTreasuryPaymentTerm)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
