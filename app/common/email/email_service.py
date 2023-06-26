from django.core.mail import EmailMessage
from app import settings


class EmailService:
    @staticmethod
    def send_email(subject, message, to_email, from_email=None, html_message=None):
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
            return email.send(fail_silently=False)
        except Exception as e:

            print(f'Error sending email: {e}')
            return None
