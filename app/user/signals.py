from django.dispatch import Signal

reset_password_signal = Signal()

user_created_signal = Signal()

user_activated_signal = Signal()

user_created_by_admin_signal = Signal()