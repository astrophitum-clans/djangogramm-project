from django.apps import AppConfig
from django.dispatch import Signal
from .utilities import send_confirmation_email


class DjangogrammConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djangogramm'


user_signup = Signal(providing_args=['instance'])


def user_signup_dispatcher(sender, **kwargs):
    """Signal dispatcher for send confirmation email"""
    send_confirmation_email(kwargs['instance'])


user_signup.connect(user_signup_dispatcher)
