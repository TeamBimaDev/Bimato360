import uuid
from datetime import datetime, timedelta
from decimal import Decimal

from common.enums.transaction_enum import PaymentTermType
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


class SalePurchaseService:
    @staticmethod
    def generate_unique_number(sale_or_purchase, quotation_order_invoice):
        first_char = "B"
        second_char = "S" if sale_or_purchase == "sale" else "P"
        third_char = {
            "quotation": "Q",
            "order": "O",
            "invoice": "I",
            "credit_note": "C"
        }.get(quotation_order_invoice, "Q")
        year = datetime.now().year
        random_string = get_random_string(length=12, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        unique_number = f"{first_char}{second_char}{third_char}_{year}_{random_string}"
        return unique_number

    @staticmethod
    def validate_data(sale_or_purchase, quotation_order_invoice):
        if not sale_or_purchase or not quotation_order_invoice:
            raise ValidationError(_('Please provide all needed data'))

    @staticmethod
    def calculate_due_date(date, payment_term_type):
        if payment_term_type == PaymentTermType.IMMEDIATE.name:
            return date
        elif payment_term_type == PaymentTermType.AFTER_ONE_WEEK.name:
            return date + timedelta(weeks=1)
        elif payment_term_type == PaymentTermType.AFTER_TWO_WEEK.name:
            return date + timedelta(weeks=2)
        elif payment_term_type == PaymentTermType.END_OF_MONTH.name:
            next_month = date.replace(day=1) + relativedelta(day=31)
            return next_month
        elif payment_term_type == PaymentTermType.NEXT_MONTH.name:
            next_month = date + relativedelta(months=1)
            return next_month
        else:
            return None

    @staticmethod
    def sale_document_custom_payment_terms_type_calculate_due_date(document):
        current_date = timezone.now().date()
        due_dates_within_month = []
        payment_schedule = document.payment_terms.payment_term_details.all().order_by('id')
        next_due_date = document.date

        for schedule in payment_schedule:
            next_due_date = SalePurchaseService.calculate_due_date(next_due_date, schedule.value)
            if next_due_date > current_date and (next_due_date - current_date).days <= 30:
                due_dates_within_month.append(next_due_date)

        return due_dates_within_month

    @staticmethod
    def sale_document_not_custom_payment_terms_type_calculate_due_date(document):
        return SalePurchaseService.calculate_due_date(document.date, document.payment_terms.type)

    @staticmethod
    def calculate_payment_late_type_custom(document, re_save=True):
        current_date = timezone.now().date()
        due_dates = []
        payment_schedule = document.payment_terms.payment_term_details.all().order_by('id')

        next_due_date = document.date

        for schedule in payment_schedule:
            next_due_date = SalePurchaseService.calculate_due_date(next_due_date, schedule.value)
            due_dates.append({next_due_date: schedule.percentage})
            if next_due_date > current_date:
                break

        document.next_due_date = next_due_date

        percentage_to_pay = 0
        is_payment_late = False
        amount_paid = document.calculate_sum_amount_paid()
        for due_date_entry in due_dates:
            due_date, percentage = list(due_date_entry.items())[0]
            percentage_to_pay += percentage

            if amount_paid < (Decimal(percentage_to_pay) / 100) * document.total_amount:
                if current_date > due_date:
                    days_in_late = abs((current_date - due_date).days)
                    document.days_in_late = days_in_late
                    is_payment_late = True if days_in_late > 0 else False
                    document.is_payment_late = True if days_in_late > 0 else False
                    break

        if not document.next_due_date or not is_payment_late:
            document.is_payment_late = False
            document.days_in_late = 0

        if re_save:
            document.skip_child_validation_form_transaction = True
            document.save()
            document.skip_child_validation_form_transaction = False

    @staticmethod
    def calculate_payment_late_type_not_custom(document, re_save=True):
        due_date = SalePurchaseService.calculate_due_date(document.date, document.payment_terms.type)
        document.next_due_date = due_date
        now = timezone.now().date()

        if due_date and now > due_date:
            amount_pad = document.calculate_sum_amount_paid()
            if amount_pad < document.total_amount:
                document.is_payment_late = True
                document.days_in_late = (now - due_date).days
            else:
                document.is_payment_late = False
                document.days_in_late = 0
        else:
            document.is_payment_late = False
            document.days_in_late = 0
        if re_save:
            document.skip_child_validation_form_transaction = True
            document.save()
            document.skip_child_validation_form_transaction = False

    @staticmethod
    def generate_random_name_file(public_id):
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        random_str = uuid.uuid4().hex[:6]
        return f"{public_id}_{current_time}_{random_str}.pdf"
