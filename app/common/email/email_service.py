from smtplib import SMTPException
from django.core.mail import EmailMessage
from app import settings
import logging
from celery import shared_task
import time
from celery import states


class EmailService:
    @staticmethod
    @shared_task(bind=True, max_retries=3, soft_time_limit=500)
    def send_email(self, subject, message, to_email, html_message=None):
        start_time = time.time()
        logger = logging.getLogger(__name__)
        logger.info(
            f'Starting task with id {self.request.id}, - send email to {to_email}, retries: {self.request.retries}')

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
            self.update_state(state=states.SUCCESS)
            end_time = time.time()
            logger.info(f'Task {self.request.id} completed in {end_time - start_time} seconds.')
        except SMTPException as e:
            logger.error(f'SMTP Error sending email: {e}')
            self.update_state(state=states.FAILURE, meta={'exc': str(e)})
            raise
        except Exception as e:
            logger.error(f'Unexpected error sending email: {e}')
            self.update_state(state=states.FAILURE, meta={'exc': str(e)})
            raise
