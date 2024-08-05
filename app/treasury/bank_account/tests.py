<<<<<<< HEAD
from core.bank.factories import BimaCoreBankFactory
from core.currency.factories import BimaCoreCurrencyFactory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory
from .models import BimaTreasuryBankAccount
from company.factories import BimaCompanyFactory
from company.models import BimaCompany
from erp.partner.factories import BimaErpPartnerFactory
from erp.partner.models import BimaErpPartner

from hr.employee.factories import BimaHrEmployeeFactory
from hr.employee.models import BimaHrEmployee


class BimaTreasuryBankAccountTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.bank = BimaCoreBankFactory.create()
        self.currency = BimaCoreCurrencyFactory.create()
        permission = Permission.objects.get(codename='treasury.bank_account.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='company.company.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.bank_account.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.bank_account.can_delete')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.bank_account.can_read')
        self.user.user_permissions.add(permission)
        self.client.force_authenticate(self.user)

        self.bank_account_data = {
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

    def test_add_bank_account_for_company(self):
        BimaCompanyFactory.create()
        self.company = BimaCompany.objects.first()
        print(self.company)
        public_id = str(self.company.public_id)
        print(public_id)
        url2 = reverse('bimacompany-list') + f'{public_id}/bank_account/'
        self.bank_account_data['parent_type'] = ContentType.objects.get_for_model(self.company).id
        self.bank_account_data['parent_id'] = self.company.id
        response = self.client.post(url2, self.bank_account_data, format='json')
        print(self.bank_account_data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryBankAccount.objects.count(), 1)
    def test_add_bank_account_for_partner(self):
        BimaErpPartnerFactory.create()
        self.partner = BimaErpPartner.objects.first()
        public_id = self.partner.public_id
        url2 = reverse('erp:bimaerppartner-list') + f'{public_id}/bank_account/'
        self.bank_account_data['parent_type'] = ContentType.objects.get_for_model(self.partner).id
        self.bank_account_data['parent_id'] = self.partner.id
        response = self.client.post(url2, self.bank_account_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryBankAccount.objects.count(), 1)
    def test_add_bank_account_for_employee(self):
        BimaHrEmployeeFactory.create()
        self.employee = BimaHrEmployee.objects.first()
        public_id = self.employee.public_id
        url2 = reverse('erp:bimaerppartner-list') + f'{public_id}/bank_account/'
        self.bank_account_data['parent_type'] = ContentType.objects.get_for_model(self.employee).id
        self.bank_account_data['parent_id'] = self.employee.id
        response = self.client.post(url2, self.bank_account_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryBankAccount.objects.count(), 1)
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
            ('company.company.can_create', 'Can create company'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaTreasuryBankAccount)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
=======
from core.bank.factories import BimaCoreBankFactory
from core.currency.factories import BimaCoreCurrencyFactory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory
from .models import BimaTreasuryBankAccount
from company.factories import BimaCompanyFactory
from company.models import BimaCompany
from erp.partner.factories import BimaErpPartnerFactory
from erp.partner.models import BimaErpPartner

from hr.employee.factories import BimaHrEmployeeFactory
from hr.employee.models import BimaHrEmployee


class BimaTreasuryBankAccountTest(APITestCase):

    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.bank = BimaCoreBankFactory.create()
        self.currency = BimaCoreCurrencyFactory.create()
        permission = Permission.objects.get(codename='treasury.bank_account.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='company.company.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.bank_account.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.bank_account.can_delete')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.bank_account.can_read')
        self.user.user_permissions.add(permission)
        self.client.force_authenticate(self.user)

        self.bank_account_data = {
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

    def test_add_bank_account_for_company(self):
        BimaCompanyFactory.create()
        self.company = BimaCompany.objects.first()
        print(self.company)
        public_id = str(self.company.public_id)
        print(public_id)
        url2 = reverse('bimacompany-list') + f'{public_id}/bank_account/'
        self.bank_account_data['parent_type'] = ContentType.objects.get_for_model(self.company).id
        self.bank_account_data['parent_id'] = self.company.id
        response = self.client.post(url2, self.bank_account_data, format='json')
        print(self.bank_account_data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryBankAccount.objects.count(), 1)
    def test_add_bank_account_for_partner(self):
        BimaErpPartnerFactory.create()
        self.partner = BimaErpPartner.objects.first()
        public_id = self.partner.public_id
        url2 = reverse('erp:bimaerppartner-list') + f'{public_id}/bank_account/'
        self.bank_account_data['parent_type'] = ContentType.objects.get_for_model(self.partner).id
        self.bank_account_data['parent_id'] = self.partner.id
        response = self.client.post(url2, self.bank_account_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryBankAccount.objects.count(), 1)
    def test_add_bank_account_for_employee(self):
        BimaHrEmployeeFactory.create()
        self.employee = BimaHrEmployee.objects.first()
        public_id = self.employee.public_id
        url2 = reverse('erp:bimaerppartner-list') + f'{public_id}/bank_account/'
        self.bank_account_data['parent_type'] = ContentType.objects.get_for_model(self.employee).id
        self.bank_account_data['parent_id'] = self.employee.id
        response = self.client.post(url2, self.bank_account_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryBankAccount.objects.count(), 1)
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
            ('company.company.can_create', 'Can create company'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaTreasuryBankAccount)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
>>>>>>> origin/ma-branch
