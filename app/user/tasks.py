from common.email.email_service import EmailService
from celery import shared_task


@shared_task(max_retries=3)
def send_email_async(mail_subject, message, email):
    EmailService.send_email.delay(mail_subject, message, email, html_message=None)
