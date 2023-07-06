from smtplib import SMTPException
from django.core.mail import EmailMessage
from app import settings
import logging
# from tenacity import retry, stop_after_attempt,
from celery import shared_task


class EmailService:
    @staticmethod
    # @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
    @shared_task(bind=True, max_retries=3, soft_time_limit=500)
    def send_email(subject, message, to_email, from_email=None, html_message=None):
        logger = logging.getLogger(__name__)
        if not from_email:
            from_email = settings.DEFAULT_FROM_EMAIL

        email = EmailMessage(
            subject,
            message,
            from_email,
            [to_email],
        )

        if html_message:
            email.content_subtype = 'html'

        try:
            email.send(fail_silently=False)
            logger.info(f'Email sent successfully: {email}')
        except SMTPException as e:
            logger.error(f'SMTP Error sending email: {e}')
            raise
        except Exception as e:
            logger.error(f'Unexpected error sending email: {e}')
            raise
