from common.enums.transaction_enum import PaymentTermType
from common.service.template_notification_service import BimaTemplateNotificationService

from .models import BimaCoreNotificationTemplate


class BimaCoreNotificationTemplateService:
    @staticmethod
    def get_notification_template_by_code(code):
        return BimaCoreNotificationTemplate.objects.filter(notification_type__code=code).first()

    @staticmethod
    def get_rendered_template_for_sale_document(sale_document, template):
        amount_paid = sale_document.calculate_sum_amount_paid()
        due_date = []
        try:
            due_date = sale_document.get_all_due_date()
            if sale_document.payment_terms.type != PaymentTermType.CUSTOM.name:
                due_date = [{due_date: 100}]
        except Exception as ex:
            pass
        data_to_send = {
            'partner_name': sale_document.partner.partner_full_name,
            'invoice_number': sale_document.number,
            'company_name': 'BimaTech',  # TODO this need to be replaced
            'due_date': due_date,
            'total_amount_paid': sale_document.amount_paid,
            'total_amount': sale_document.total_amount,
            'amount_remaining': (sale_document.total_amount - amount_paid)
        }
        message = BimaTemplateNotificationService.replace_variables_in_template(template.message, data_to_send)
        subject = BimaTemplateNotificationService.replace_variables_in_template(template.subject,
                                                                                {
                                                                                    'invoice_number': sale_document.number})

        return subject, message
