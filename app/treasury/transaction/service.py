import logging
import os

import pandas as pd
from common.enums.transaction_enum import TransactionDirection
from common.enums.transaction_enum import TransactionNature
from django.db import models
from django.db.models import Sum, Case, When, F
from treasury.transaction_type.models import BimaTreasuryTransactionType

from app import settings

logger = logging.getLogger(__name__)


class BimaTreasuryTransactionService:
    def __init__(self, queryset):
        self.queryset = queryset

    def calculate_sums(self):
        aggregations = self.queryset.aggregate(
            total_income=Sum(
                Case(
                    When(direction=TransactionDirection.INCOME.name, then=F("amount")),
                    output_field=models.DecimalField(),
                )
            ),
            total_outcome=Sum(
                Case(
                    When(direction=TransactionDirection.OUTCOME.name, then=F("amount")),
                    output_field=models.DecimalField(),
                )
            ),
        )

        total_income = aggregations.get("total_income") or 0
        total_outcome = aggregations.get("total_outcome") or 0
        difference = total_income - total_outcome

        return {
            "total_income": total_income,
            "total_outcome": total_outcome,
            "difference": difference,
        }

    def format_data_for_export(self):
        data = []
        for transaction in self.queryset:
            try:
                row = {
                    "Nature": transaction.nature,
                    "Direction": transaction.direction,
                    "Transaction Type": transaction.transaction_type,
                    "Note": transaction.note,
                    "Date": transaction.date,
                    "Expected Date": transaction.expected_date,
                    "Amount": transaction.amount,
                    "Transaction Source": transaction.transaction_source,
                    "Bank Account Number": transaction.partner_bank_account_number,
                    "Partner": self._get_partner_name(transaction.partner),
                    "Cash": transaction.cash.cash_name if transaction.cash else "",
                    "Bank Account": self._get_bank_account_name(
                        transaction.bank_account
                    ),
                }
                data.append(row)
            except Exception as e:
                logger.error(
                    f"Error processing transaction {transaction.public_id}. Error: {e}"
                )
        return data

    def _get_partner_name(self, partner):
        if partner.partner_type == "INDIVIDUAL":
            return f"{partner.first_name} {partner.last_name}"
        else:
            return partner.company_name

    def _get_bank_account_name(self, bank_account):
        if bank_account:
            return f"{bank_account.name} ({bank_account.account_number})"
        return ""

    def export_to_csv(self, file_name):
        data = self.format_data_for_export()
        df = pd.DataFrame(data)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        df.to_csv(file_path, index=False)
        return file_path

    def export_to_excel(self, file_name):
        data = self.format_data_for_export()
        df = pd.DataFrame(data)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        df.to_excel(file_path, index=False, engine="openpyxl")
        return file_path

    @staticmethod
    def create_auto_transaction(transaction):
        from .models import BimaTreasuryTransaction

        complementary_transaction_mappings = {
            ("FROM_CASH_TO_ACCOUNT_OUTCOME", "OUTCOME"): (
                "FROM_CASH_TO_ACCOUNT_INCOME",
                "INCOME",
            ),
            ("FROM_ACCOUNT_TO_CASH_OUTCOME", "OUTCOME"): (
                "FROM_ACCOUNT_TO_CASH_INCOME",
                "INCOME",
            ),
        }

        key = (transaction.transaction_type.code, transaction.direction)
        if key not in complementary_transaction_mappings:
            return

        (
            complementary_code,
            complementary_direction,
        ) = complementary_transaction_mappings[key]

        complementary_transaction_type = BimaTreasuryTransactionType.objects.get(
            code=complementary_code, income_outcome=complementary_direction
        )

        if transaction.nature == TransactionNature.CASH.name:
            params = {
                "nature": "BANK",
                "direction": "INCOME",
                "transaction_type": complementary_transaction_type,
                "bank_account": transaction.bank_account,
                "date": transaction.date,
                "amount": transaction.amount,
                "transaction_source": transaction,
            }
        elif transaction.nature == TransactionNature.BANK.name:
            params = {
                "nature": "CASH",
                "direction": "INCOME",
                "transaction_type": complementary_transaction_type,
                "cash": transaction.cash,
                "date": transaction.date,
                "amount": transaction.amount,
                "transaction_source": transaction,
            }

        created_transaction = BimaTreasuryTransaction.objects.create(**params)
        logger.info(
            f"Auto transaction {created_transaction.pk} created for transaction {transaction.pk}"
        )
        return created_transaction


class TransactionEffectStrategy:
    def apply(self, transaction):
        raise NotImplementedError

    def revert(self, transaction):
        raise NotImplementedError


class CashTransactionEffectStrategy(TransactionEffectStrategy):
    def apply(self, transaction):
        transaction.cash.balance += (
            transaction.amount
            if transaction.direction == TransactionNature.INCOME.name
            else -transaction.amount
        )
        transaction.cash.save()

    def revert(self, transaction):
        transaction.cash.balance -= (
            transaction.amount
            if transaction.direction == TransactionNature.INCOME.name
            else +transaction.amount
        )
        transaction.cash.save()


class BankTransactionEffectStrategy(TransactionEffectStrategy):
    def apply(self, transaction):
        transaction.bank_account.balance += (
            transaction.amount
            if transaction.direction == TransactionNature.INCOME.name
            else -transaction.amount
        )
        transaction.bank_account.save()

    def revert(self, transaction):
        transaction.bank_account.balance -= (
            transaction.amount
            if transaction.direction == TransactionNature.INCOME.name
            else +transaction.amount
        )
        transaction.bank_account.save()
