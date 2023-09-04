import logging
from collections import defaultdict
from datetime import datetime

import pandas as pd
from common.enums.transaction_enum import TransactionDirection, TransactionNature
from django.db import models
from django.db.models import Sum, Case, When, F
from django.utils.crypto import get_random_string
from erp.partner.models import BimaErpPartner
from openpyxl.styles import Border, Side, Font
from openpyxl.utils import get_column_letter
from treasury.bank_account.models import BimaTreasuryBankAccount
from treasury.cash.models import BimaTreasuryCash
from treasury.payment_method.models import BimaTreasuryPaymentMethod
from treasury.transaction_type.models import BimaTreasuryTransactionType

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
                    "Transaction Type": transaction.transaction_type.name,
                    "Note": transaction.note,
                    "Date": transaction.date,
                    "Expected Date": transaction.expected_date,
                    "Amount": transaction.amount,
                    "Transaction Source": transaction.transaction_source,
                    "Bank Account Number": transaction.partner_bank_account_number,
                    "Partner": self._get_partner_name(transaction.partner),
                    "Cash": transaction.cash.name if transaction.cash else "",
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
        if partner:
            if partner.partner_type == "INDIVIDUAL":
                return f"{partner.first_name} {partner.last_name}"
            else:
                return partner.company_name
        return ""

    def _get_bank_account_name(self, bank_account):
        if bank_account:
            return f"{bank_account.name} ({bank_account.account_number})"
        return ""

    def export_to_csv(self):
        data = self.format_data_for_export()
        return pd.DataFrame(data)

    def export_to_excel(self):
        data = self.format_data_for_export()
        return pd.DataFrame(data)

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
        payment_method_for_cash = BimaTreasuryPaymentMethod.objects.get(
            code="CASH_PAYMENT_INCOME", income_outcome="INCOME"
        )
        payment_method_for_bank = BimaTreasuryPaymentMethod.objects.get(
            code="TRANSFER_INCOME", income_outcome="INCOME"
        )
        number = BimaTreasuryTransactionService.generate_unique_number(),
        if transaction.nature == TransactionNature.CASH.name:
            params = {
                "number": number,
                "nature": "BANK",
                "direction": "INCOME",
                "transaction_type": complementary_transaction_type,
                "payment_method": payment_method_for_bank,
                "bank_account": transaction.bank_account,
                "cash": transaction.cash,
                "date": transaction.date,
                "amount": transaction.amount,
                "transaction_source": transaction,
                "reference": transaction.reference,
            }
        elif transaction.nature == TransactionNature.BANK.name:
            params = {
                "number": number,
                "nature": "CASH",
                "direction": "INCOME",
                "transaction_type": complementary_transaction_type,
                "payment_method": payment_method_for_cash,
                "cash": transaction.cash,
                "bank_account": transaction.bank_account,
                "date": transaction.date,
                "amount": transaction.amount,
                "transaction_source": transaction,
                "reference": transaction.reference,
            }

        created_transaction = BimaTreasuryTransaction.objects.create(**params)
        logger.info(
            f"Auto transaction {created_transaction.pk} created for transaction {transaction.pk}"
        )
        return created_transaction

    @staticmethod
    def group_by_date(history_data):
        grouped = defaultdict(list)

        for record in history_data:
            date_without_time = datetime.fromisoformat(record["history_date"]).date()
            grouped[date_without_time].append(record)

        return grouped

    def get_bank_account_name(self, value):
        obj = BimaTreasuryBankAccount.objects.filter(id=value).first()
        return obj.name if obj else None

    def get_cash_name(self, value):
        obj = BimaTreasuryCash.objects.filter(id=value).first()
        return obj.name if obj else None

    def get_transaction_type_name(self, value):
        obj = BimaTreasuryTransactionType.objects.filter(id=value).first()
        return obj.name if obj else None

    def get_partner_name(self, value):
        obj = BimaErpPartner.objects.filter(id=value).first()
        if obj:
            if obj.partner_type == "INDIVIDUAL":
                return f"{obj.first_name} {obj.last_name}"
            else:
                return obj.company_name
        return None

    FIELD_TO_METHOD_MAP = {
        "bank_account": get_bank_account_name,
        "cash": get_cash_name,
        "transaction_type": get_transaction_type_name,
        "partner": get_partner_name,
    }

    def style_worksheet(self, ws):
        thin_border = Border(
            left=Side(style="thin"),
            right=Side(style="thin"),
            top=Side(style="thin"),
            bottom=Side(style="thin"),
        )

        for row in ws.iter_rows():
            for cell in row:
                cell.border = thin_border

        for row in ws.iter_rows():
            for cell in row:
                if cell.column_letter == "B":
                    if cell.value == "INCOME":
                        amount_cell = ws[f"G{cell.row}"]
                        amount_cell.font = Font(color="00FF00")
                    elif cell.value == "OUTCOME":
                        amount_cell = ws[f"G{cell.row}"]
                        amount_cell.font = Font(color="FF0000")

        for column in ws.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = max_length + 2
            ws.column_dimensions[
                get_column_letter(column[0].column)
            ].width = adjusted_width

    def append_totals(self, ws):
        sums = self.calculate_sums()
        ws.append([])
        ws.append(["Totals"])
        ws.append(["Total Income", sums["total_income"]])
        ws.append(["Total Outcome", sums["total_outcome"]])
        ws.append(["Difference", sums["difference"]])

    @staticmethod
    def generate_unique_number():
        first_char = "B"
        second_char = "T"
        year = datetime.now().year
        random_string = get_random_string(length=12, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        unique_number = f"{first_char}{second_char}_{year}_{random_string}"
        return unique_number


class TransactionEffectStrategy:
    def apply(self, transaction):
        raise NotImplementedError

    def revert(self, transaction):
        raise NotImplementedError


class CashTransactionEffectStrategy(TransactionEffectStrategy):
    def apply(self, transaction):
        transaction.cash.balance += (
            transaction.amount
            if transaction.direction == TransactionDirection.INCOME.name
            else -transaction.amount
        )
        transaction.cash.save()

    def revert(self, transaction):
        transaction.cash.balance -= (
            transaction.amount
            if transaction.direction == TransactionDirection.INCOME.name
            else +transaction.amount
        )
        transaction.cash.save()


class BankTransactionEffectStrategy(TransactionEffectStrategy):
    def apply(self, transaction):
        transaction.bank_account.balance += (
            transaction.amount
            if transaction.direction == TransactionDirection.INCOME.name
            else -transaction.amount
        )
        transaction.bank_account.save()

    def revert(self, transaction):
        transaction.bank_account.balance -= (
            transaction.amount
            if transaction.direction == TransactionDirection.INCOME.name
            else +transaction.amount
        )
        transaction.bank_account.save()
