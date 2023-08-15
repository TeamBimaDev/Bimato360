from datetime import datetime

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
