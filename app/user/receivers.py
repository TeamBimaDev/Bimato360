import os
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode

from .signals import reset_password_signal, user_created_signal, user_activated_signal, user_created_by_admin_signal, \
    user_declined_signal
from .tasks import send_email_async
from app.settings import config


@receiver(reset_password_signal)
def send_password_reset_email(sender, **kwargs):
    email = kwargs['email']
    reset_password_link = kwargs['reset_password_link']
    context = {
        'reset_password_link': reset_password_link,
    }
    message = render_to_string('user/reset_password_email.html', context)
    mail_subject = 'Password Reset'
    html_message = True
    send_email_async.delay(mail_subject, message, email, html_message)


@receiver(post_save, sender=get_user_model())
def send_email_after_user_created(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        if getattr(instance, 'created_by_admin', False):
            user_created_by_admin_signal.send(sender=sender, user=instance)
        else:
            user_created_signal.send(sender=sender, user=instance)


@receiver(user_created_signal)
def send_user_activation_email(sender, user, **kwargs):
    admins = get_user_model().objects.filter(is_staff=True, user_permissions__codename='user.user.can_activate_account')
    for admin in admins:
        context = {
            'admin_name': admin.name,
            'user_name': user.name,
            'registration_time': user.date_joined,
            'activation_link': config('SITE_URL') + '/api/user/activate_user_account/' + str(user.public_id) + "/"
        }
        message = render_to_string('user/activation_email.html', context)
        mail_subject = 'User Activation'
        send_email_async.delay(mail_subject, message, admin.email, html_message=True)


@receiver(user_created_signal)
def send_user_creation_email(sender, user, **kwargs):
    context = {
        'user_name': user.name,
        'registration_time': user.date_joined,
        'site_url': config('SITE_URL')
    }
    message = render_to_string('user/user_creation_email_notify.html', context)
    mail_subject = 'Account Created'
    send_email_async.delay(mail_subject, message, user.email, html_message=True)


@receiver(user_created_by_admin_signal)
def send_user_created_by_admin_creation_email(sender, user, **kwargs):
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    user.reset_password_token = token
    user.reset_password_uid = uidb64
    user.reset_password_time = timezone.now()
    user.save()

    context = {
        'user_name': user.name,
        'registration_time': user.date_joined,
        'site_url': config('SITE_URL'),
        'uidb64': uidb64,
        'token': token,
        'activation_link': config('SITE_URL') + '/api/user/activate_user_account/' + str(user.public_id) + "/"
    }
    message = render_to_string('user/user_activate_account_and_change_password.html', context)
    mail_subject = 'Account Created'
    send_email_async.delay(mail_subject, message, user.email, html_message=True)


@receiver(user_activated_signal)
def send_activation_confirmation_email(sender, **kwargs):
    user = kwargs['user']
    admin = kwargs['admin']
    context = {
        'user_name': user.name,
        'admin_name': admin.name,
        'activation_time': user.approved_at,
    }
    message = render_to_string('user/activation_confirmation_email.html', context)
    mail_subject = 'Account Activation Confirmation'
    send_email_async.delay(mail_subject, message, user.email, html_message=True)


@receiver(user_declined_signal)
def send_declined_email_for_user(sender, **kwargs):
    user = kwargs['user']
    admin = kwargs['admin']
    context = {
        'user_name': user.name,
        'admin_name': admin.name,
        'activation_time': user.approved_at,
    }
    message = render_to_string('user/user_declined_email.html', context)
    mail_subject = 'Account Activation Confirmation'
    send_email_async.delay(mail_subject, message, user.email, html_message=True)
