from core.bank.factories import BimaCoreBankFactory
from core.currency.factories import BimaCoreCurrencyFactory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory

from .models import BimaTreasuryBankAccount


class BimaTreasuryBankAccountTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.bank = BimaCoreBankFactory.create()
        self.currency = BimaCoreCurrencyFactory.create()
        permission = Permission.objects.get(codename='treasury.bank_account.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.bank_account.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.bank_account.can_delete')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.bank_account.can_read')
        self.user.user_permissions.add(permission)

        self.address_data = {
            'name': 'bank account',
            'account_number': 'account_number 1',
            'iban': '12345',
            'bank_public_id': str(self.bank.public_id),
            'currency_public_id': str(self.currency.public_id),
            'balance': 12,
            'account_holder_name': 'account_holder_name 1',
            'active': True,
            'note': 'note 1',
        }
        # Give permissions to the user.
        self.client.force_authenticate(self.user)

    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('treasury:bimatreasurybankaccount-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def create_permissions(self):
        permission_list = [
            # Add your permission tuples here.
            ('treasury.bank_account.can_create', 'Can create bank account'),
            ('treasury.bank_account.can_update', 'Can update bank account'),
            ('treasury.bank_account.can_delete', 'Can delete bank account'),
            ('treasury.bank_account.can_read', 'Can read bank account'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaTreasuryBankAccount)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
