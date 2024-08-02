
from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        from .signals import reset_password_signal, user_created_signal, user_activated_signal, \
                             user_created_by_admin_signal, user_declined_signal

        from .receivers import send_password_reset_email, send_email_after_user_created, send_user_activation_email, \
            send_user_creation_email, send_user_created_by_admin_creation_email, send_activation_confirmation_email, \
            send_declined_email_for_user

