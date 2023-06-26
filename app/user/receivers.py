from django.dispatch import receiver
from django.template.loader import render_to_string
from .signals import reset_password_signal
from common.email.email_service import EmailService


@receiver(reset_password_signal)
def send_password_reset_email(sender, **kwargs):
    email = kwargs['email']
    reset_password_link = kwargs['reset_password_link']
    context = {
        'reset_password_link': reset_password_link,
    }
    message = render_to_string('reset_password_email.html', context)
    mail_subject = 'Password Reset'
    EmailService.send_email(mail_subject, message, email)
