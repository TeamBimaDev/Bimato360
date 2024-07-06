import logging
from datetime import timedelta
from decimal import Decimal

from common.enums.partner_type import PartnerType
from common.enums.transaction_enum import PaymentTermType
from common.service.purchase_sale_service import SalePurchaseService
from common.service.template_notification_service import BimaTemplateNotificationService
from django.apps import apps
from django.utils import timezone
from erp.partner.service import BimaErpPartnerService
from erp.sale_document.service import SaleDocumentService

logger = logging.getLogger(__name__)


class BimaErpNotificationService:
    @staticmethod
    def send_notification_for_payment_late_sale_documents():
        unpaid_sale_documents = SaleDocumentService.get_sale_document_for_notification(is_payment_late=True)
        sale_document_to_return = []
        for sale_document in unpaid_sale_documents:
            if not sale_document.payment_terms:
                continue
            try:
                logger.info(f"start verification payment late status sale document {sale_document.public_id}")
                BimaErpNotificationService.send_notification_payment_sale_document_based_on_payment_term_type(
                    sale_document, template_code='NOTIFICATION_PAYMENT_LATE', days_difference=1)
                sale_document_to_return.append(
                    {"sale_document_public_ud": sale_document.public_id,
                     "next_due_date": sale_document.next_due_date})
                logger.info(f"sale document verification payment late {sale_document.public_id} succeeded")
            except Exception as ex:
                logger.error(f"sale document verification payment late {sale_document.public_id} failed {ex}")

        return sale_document_to_return

    @staticmethod
    def send_notification_for_payment_reminder_sale_documents(days_before_due_date=3):
        unpaid_sale_documents = SaleDocumentService.get_sale_document_for_notification()
        sale_document_to_return = []
        for sale_document in unpaid_sale_documents:
            if not sale_document.payment_terms:
                continue
            try:
                logger.info(f"start verification payment reminder sale document {sale_document.public_id}")
                BimaErpNotificationService.send_notification_payment_sale_document_based_on_payment_term_type(
                    sale_document, template_code='NOTIFICATION_PAYMENT_REMINDER', days_difference=-days_before_due_date)
                sale_document_to_return.append(
                    {"sale_document_public_ud": sale_document.public_id,
                     "next_due_date": sale_document.next_due_date})
                logger.info(f"sale document verification payment late {sale_document.public_id} succeeded")

            except Exception as ex:
                logger.error(f"sale document verification payment reminder {sale_document.public_id} failed {ex}")

        return sale_document_to_return

    @staticmethod
    def send_notification_payment_sale_document_based_on_payment_term_type(sale_document, template_code,
                                                                           days_difference, message=None, subject=None,
                                                                           send_instantly=False):
        if sale_document.payment_terms.type != PaymentTermType.CUSTOM.name:
            BimaErpNotificationService.send_notification_sale_document_not_custom_type(
                sale_document, days_difference, template_code=template_code, message=message, subject=subject,
                send_instantly=send_instantly)
        else:
            BimaErpNotificationService.send_notification_sale_document_custom_type(
                sale_document, days_difference, template_code=template_code, message=message, subject=subject,
                send_instantly=send_instantly)

    @staticmethod
    def send_notification_sale_document_custom_type(document, days_difference, template_code, message=None,
                                                    subject=None, send_instantly=False):
        BimaCoreNotificationTemplate = apps.get_model('core', 'BimaCoreNotificationTemplate')
        current_date = timezone.now().date()
        due_dates = []
        payment_schedule = document.payment_terms.payment_term_details.all().order_by('id')
        next_due_date = document.date
        notification_template = BimaCoreNotificationTemplate.objects.filter(
            notification_type__code=template_code).first()

        for schedule in payment_schedule:
            next_due_date = SalePurchaseService.calculate_due_date(next_due_date, schedule.value)
            due_dates.append({next_due_date: schedule.percentage})
            if next_due_date > current_date:
                break

        percentage_to_pay = 0
        send_notification = False
        amount_paid = document.calculate_sum_amount_paid()
        for due_date_entry in due_dates:
            due_date, percentage = list(due_date_entry.items())[0]
            percentage_to_pay += percentage

            if ((amount_paid < (Decimal(percentage_to_pay) / 100) * document.total_amount) and
                    (current_date == due_date + timedelta(days=days_difference))):
                send_notification = True

        if send_notification or send_instantly:
            data_to_send = {
                'partner_name': document.partner.first_name if document.partner.partner_type == PartnerType.INDIVIDUAL.name else document.partner.company_name,
                'invoice_number': document.number,
                'company_name': 'BimaTech',  # TODO this need to be replaced
                'due_date': due_dates,
                'total_amount_paid': amount_paid,
                'total_amount': document.total_amount,
                'amount_remaining': (document.total_amount - amount_paid),
                'file_url': document.last_generated_file_url,
                'message': message,
                'subject': subject
            }
            BimaErpNotificationService.send_notification_payment_late(notification_template, document, data_to_send)

    @staticmethod
    def send_notification_sale_document_not_custom_type(document, days_difference, template_code, message=None,
                                                        subject=None, send_instantly=False):

        due_date = SalePurchaseService.calculate_due_date(document.date, document.payment_terms.type)
        send_notification = False
        now = timezone.now().date()

        BimaCoreNotificationTemplate = apps.get_model('core', 'BimaCoreNotificationTemplate')
        notification_template = BimaCoreNotificationTemplate.objects.filter(
            notification_type__code=template_code).first()
        amount_paid = 0

        if due_date and now == due_date + timedelta(days=days_difference):
            amount_paid = document.calculate_sum_amount_paid()
            if amount_paid < document.total_amount:
                send_notification = True

        if send_notification or send_instantly:
            data_to_send = {
                'partner_name': document.partner.first_name if document.partner.partner_type == PartnerType.INDIVIDUAL.name else document.partner.company_name,
                'invoice_number': document.number,
                'company_name': 'BimaTech',  # TODO this need to be replaced
                'due_date': [{due_date: 100}],
                'total_amount_paid': amount_paid,
                'total_amount': document.total_amount,
                'amount_remaining': (document.total_amount - amount_paid),
                'file_url': document.last_generated_file_url,
                'message': message,
                'subject': subject
            }
            BimaErpNotificationService.send_notification_payment_late(notification_template, document, data_to_send)

    @staticmethod
    def send_notification_payment_late(notification_template, document, data_to_send):
        partner_contacts = BimaErpPartnerService.get_partner_contacts(document.partner)
        receivers = [contact.email for contact in partner_contacts if contact.email]
        if document.partner.email:
            receivers.append(document.partner.email)
        data = {
            'subject': data_to_send['subject'] if data_to_send['subject'] is not None
            else BimaTemplateNotificationService.replace_variables_in_template(notification_template.subject,
                                                                               {'invoice_number': document.number}),
            'message': data_to_send['message'] if data_to_send['message'] is not None
            else BimaTemplateNotificationService.replace_variables_in_template(notification_template.message,
                                                                               data_to_send),
            'receivers': receivers,
            'attachments': [data_to_send['file_url']],
            'notification_type_id': notification_template.notification_type.id,
            'sender': None,
            'app_name': 'erp',
            'model_name': 'bimaerpsaledocument',
            'parent_id': document.id
        }
        BimaTemplateNotificationService.send_email_and_save_notification.delay(data)
