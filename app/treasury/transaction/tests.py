<<<<<<< HEAD
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory
from .factories import BimaTreasuryBankAccountFactory
from erp.partner.factories import BimaErpPartnerFactory
from treasury.transaction_type.factories import BimaTreasuryTransactionTypeFactory
from treasury.payment_method.factories import BimaTreasuryPaymentMethodFactory
from treasury.cash.factories import BimaTreasuryCashFactory
from .models import BimaTreasuryTransaction


class BimaTreasuryTransactionTest(APITestCase):
    def create_common_transaction_data_cash(self, direction):
        return {
            "number": 123456,
            "nature": "CASH",
            "direction": direction,
            "transaction_type_public_id": str(self.transaction_type.public_id),
            "payment_method_public_id": str(self.payment_method.public_id),
            "cash_public_id": str(self.cash.public_id),
            "partner_public_id": str(self.partner.public_id),
            "note": "Transaction Note",
            "date": "2023-10-03",
            "expected_date": "2023-11-02",
            "amount": 12345.678,
            "remaining_amount": 9876543.210,
            "reference": "Reference Text",
            "transaction_source_public_id": None,
            "partner_bank_account_number": "9876543210",
        }
    def create_common_transaction_data_bank(self, direction):
        return {
            "number": 123456,
            "nature": "BANK",
            "direction": direction,
            "transaction_type_public_id": str(self.transaction_type.public_id),
            "payment_method_public_id": str(self.payment_method.public_id),
            "partner_public_id": str(self.partner.public_id),
            "bank_account_public_id": str(self.bank_account.public_id),
            "note": "Transaction Note",
            "date": "2023-10-03",
            "expected_date": "2023-11-02",
            "amount": 12345.678,
            "remaining_amount": 9876543.210,
            "reference": "Reference Text",
            "transaction_source_public_id": None,
            "partner_bank_account_number": "9876543210",
        }
    def setUp(self):

        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.transaction_type = BimaTreasuryTransactionTypeFactory.create(active=True)
        self.payment_method = BimaTreasuryPaymentMethodFactory.create(active=True)
        self.cash = BimaTreasuryCashFactory.create(active=True)
        self.partner = BimaErpPartnerFactory.create()
        self.bank_account = BimaTreasuryBankAccountFactory.create(active=True)
        permission = Permission.objects.get(codename='treasury.transaction.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.transaction.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.transaction.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.transaction.can_delete')
        self.user.user_permissions.add(permission)
        self.client.force_authenticate(self.user)
        self.transaction_data_cash = self.create_common_transaction_data_cash("INCOME")
        self.transaction_data_bank = self.create_common_transaction_data_bank("INCOME")
    def create_transaction_cash_income(self):
        url = reverse('treasury:bimatreasurytransaction-list')
        response = self.client.post(url, self.transaction_data_cash, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryTransaction.objects.count(), 1)
    def test_create_transaction_cash_income(self):
        url = reverse('treasury:bimatreasurytransaction-list')
        response = self.client.post(url, self.transaction_data_cash, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryTransaction.objects.count(), 1)

    def test_create_transaction_cash_outcome(self):
        self.transaction_data_cash["direction"] = "OUTCOME"
        url = reverse('treasury:bimatreasurytransaction-list')
        response = self.client.post(url, self.transaction_data_cash, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryTransaction.objects.count(), 1)
    def test_create_transaction_bank_income(self):
        url = reverse('treasury:bimatreasurytransaction-list')
        response = self.client.post(url, self.transaction_data_bank, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryTransaction.objects.count(), 1)

    def test_create_transaction_bank_outcome(self):
        self.transaction_data_bank["direction"] = "OUTCOME"
        url = reverse('treasury:bimatreasurytransaction-list')
        response = self.client.post(url, self.transaction_data_bank, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryTransaction.objects.count(), 1)

    def test_get_transaction_cash_income(self):
        self.create_transaction_cash_income()
        url = reverse('treasury:bimatreasurytransaction-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

    def test_update_transaction_cash_income(self):
        self.create_transaction_cash_income()
        transaction = BimaTreasuryTransaction.objects.first()
        url = reverse('treasury:bimatreasurytransaction-detail', kwargs={'pk': str(transaction.public_id)})
        data = {'number': 215487}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaTreasuryTransaction.objects.get(pk=transaction.pk).number, '215487')

    def test_delete_transaction_cash_income(self):
        self.create_transaction_cash_income()
        transaction = BimaTreasuryTransaction.objects.first()
        url = reverse('treasury:bimatreasurytransaction-detail', kwargs={'pk': str(transaction.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('treasury:bimatreasurytransaction-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('treasury:bimatreasurytransaction-list')
        response = self.client.post(url, self.transaction_data_bank, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.create_transaction_cash_income()
        transaction = BimaTreasuryTransaction.objects.first()
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        url = reverse('treasury:bimatreasurytransaction-detail', kwargs={'pk': str(transaction.public_id)})
        data = {'number': 154714}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.create_transaction_cash_income()
        transaction = BimaTreasuryTransaction.objects.first()
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        url = reverse('treasury:bimatreasurytransaction-detail', kwargs={'pk': str(transaction.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def create_permissions(self):
        permission_list = [
            ('treasury.transaction.can_create', 'Can create transaction'),
            ('treasury.transaction.can_update', 'Can update transaction'),
            ('treasury.transaction.can_delete', 'Can delete transaction'),
            ('treasury.transaction.can_read', 'Can read transaction'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaTreasuryTransaction)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
=======
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.factories import UserFactory
from .factories import BimaTreasuryBankAccountFactory
from erp.partner.factories import BimaErpPartnerFactory
from treasury.transaction_type.factories import BimaTreasuryTransactionTypeFactory
from treasury.payment_method.factories import BimaTreasuryPaymentMethodFactory
from treasury.cash.factories import BimaTreasuryCashFactory
from .models import BimaTreasuryTransaction


class BimaTreasuryTransactionTest(APITestCase):
    def create_common_transaction_data_cash(self, direction):
        return {
            "number": 123456,
            "nature": "CASH",
            "direction": direction,
            "transaction_type_public_id": str(self.transaction_type.public_id),
            "payment_method_public_id": str(self.payment_method.public_id),
            "cash_public_id": str(self.cash.public_id),
            "partner_public_id": str(self.partner.public_id),
            "note": "Transaction Note",
            "date": "2023-10-03",
            "expected_date": "2023-11-02",
            "amount": 12345.678,
            "remaining_amount": 9876543.210,
            "reference": "Reference Text",
            "transaction_source_public_id": None,
            "partner_bank_account_number": "9876543210",
        }
    def create_common_transaction_data_bank(self, direction):
        return {
            "number": 123456,
            "nature": "BANK",
            "direction": direction,
            "transaction_type_public_id": str(self.transaction_type.public_id),
            "payment_method_public_id": str(self.payment_method.public_id),
            "partner_public_id": str(self.partner.public_id),
            "bank_account_public_id": str(self.bank_account.public_id),
            "note": "Transaction Note",
            "date": "2023-10-03",
            "expected_date": "2023-11-02",
            "amount": 12345.678,
            "remaining_amount": 9876543.210,
            "reference": "Reference Text",
            "transaction_source_public_id": None,
            "partner_bank_account_number": "9876543210",
        }
    def setUp(self):

        self.create_permissions()
        self.client = APIClient()
        self.user = UserFactory()
        self.transaction_type = BimaTreasuryTransactionTypeFactory.create(active=True)
        self.payment_method = BimaTreasuryPaymentMethodFactory.create(active=True)
        self.cash = BimaTreasuryCashFactory.create(active=True)
        self.partner = BimaErpPartnerFactory.create()
        self.bank_account = BimaTreasuryBankAccountFactory.create(active=True)
        permission = Permission.objects.get(codename='treasury.transaction.can_create')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.transaction.can_read')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.transaction.can_update')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='treasury.transaction.can_delete')
        self.user.user_permissions.add(permission)
        self.client.force_authenticate(self.user)
        self.transaction_data_cash = self.create_common_transaction_data_cash("INCOME")
        self.transaction_data_bank = self.create_common_transaction_data_bank("INCOME")
    def create_transaction_cash_income(self):
        url = reverse('treasury:bimatreasurytransaction-list')
        response = self.client.post(url, self.transaction_data_cash, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryTransaction.objects.count(), 1)
    def test_create_transaction_cash_income(self):
        url = reverse('treasury:bimatreasurytransaction-list')
        response = self.client.post(url, self.transaction_data_cash, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryTransaction.objects.count(), 1)

    def test_create_transaction_cash_outcome(self):
        self.transaction_data_cash["direction"] = "OUTCOME"
        url = reverse('treasury:bimatreasurytransaction-list')
        response = self.client.post(url, self.transaction_data_cash, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryTransaction.objects.count(), 1)
    def test_create_transaction_bank_income(self):
        url = reverse('treasury:bimatreasurytransaction-list')
        response = self.client.post(url, self.transaction_data_bank, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryTransaction.objects.count(), 1)

    def test_create_transaction_bank_outcome(self):
        self.transaction_data_bank["direction"] = "OUTCOME"
        url = reverse('treasury:bimatreasurytransaction-list')
        response = self.client.post(url, self.transaction_data_bank, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaTreasuryTransaction.objects.count(), 1)

    def test_get_transaction_cash_income(self):
        self.create_transaction_cash_income()
        url = reverse('treasury:bimatreasurytransaction-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

    def test_update_transaction_cash_income(self):
        self.create_transaction_cash_income()
        transaction = BimaTreasuryTransaction.objects.first()
        url = reverse('treasury:bimatreasurytransaction-detail', kwargs={'pk': str(transaction.public_id)})
        data = {'number': 215487}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaTreasuryTransaction.objects.get(pk=transaction.pk).number, '215487')

    def test_delete_transaction_cash_income(self):
        self.create_transaction_cash_income()
        transaction = BimaTreasuryTransaction.objects.first()
        url = reverse('treasury:bimatreasurytransaction-detail', kwargs={'pk': str(transaction.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    def test_unauthenticated(self):
        self.client.logout()
        url = reverse('treasury:bimatreasurytransaction-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create(self):
        self.client.logout()
        self.client.force_authenticate(UserFactory())
        url = reverse('treasury:bimatreasurytransaction-list')
        response = self.client.post(url, self.transaction_data_bank, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        self.create_transaction_cash_income()
        transaction = BimaTreasuryTransaction.objects.first()
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        url = reverse('treasury:bimatreasurytransaction-detail', kwargs={'pk': str(transaction.public_id)})
        data = {'number': 154714}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        self.create_transaction_cash_income()
        transaction = BimaTreasuryTransaction.objects.first()
        self.client.logout()
        user_without_permission = UserFactory()
        self.client.force_authenticate(user_without_permission)
        url = reverse('treasury:bimatreasurytransaction-detail', kwargs={'pk': str(transaction.public_id)})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def create_permissions(self):
        permission_list = [
            ('treasury.transaction.can_create', 'Can create transaction'),
            ('treasury.transaction.can_update', 'Can update transaction'),
            ('treasury.transaction.can_delete', 'Can delete transaction'),
            ('treasury.transaction.can_read', 'Can read transaction'),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(BimaTreasuryTransaction)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
>>>>>>> origin/ma-branch
