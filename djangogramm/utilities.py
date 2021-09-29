from django.core.signing import Signer
from django.template.loader import render_to_string
from django_djangogramm.settings import ALLOWED_HOSTS

signer = Signer()


def send_confirmation_email(user):
    """send confirmation emails to user"""
    if ALLOWED_HOSTS:
        host = f'http://{ALLOWED_HOSTS[0]}'
    else:
        host = 'http://127.0.0.1:8000'
    context = {
        'user': user,
        'host': host,
        'sign': signer.sign(user.get_username())
    }
    subject = render_to_string('emails/activation_letter_subject.html', context)
    body_text = render_to_string('emails/activation_letter_body.html', context)
    user.email_user(subject, body_text)
