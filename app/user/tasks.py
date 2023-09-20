from celery import shared_task
from common.email.email_service import EmailService


@shared_task(max_retries=3)
def send_email_async(mail_subject, message, email, html_message=None):
    EmailService.send_email.delay(mail_subject, message, email, attachments=None, html_message=html_message)
