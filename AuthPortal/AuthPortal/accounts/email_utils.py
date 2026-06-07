"""
Email utility for sending registration credentials.

Uses EmailMultiAlternatives to send both plain text and HTML versions.
The HTML version is rendered from templates/email/welcome.html.
"""
import logging

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

logger = logging.getLogger('accounts')

LOGIN_URL = 'http://127.0.0.1:8000/'


def send_welcome_email(first_name, last_name, email, password):
    """
    Send a welcome email with login credentials to a newly registered user.

    Sends both:
    - Plain text version (for basic email clients)
    - HTML version (for Gmail, Outlook, etc.)

    Returns:
        True if email was sent successfully, False otherwise.
    """
    subject = 'Welcome to RDSO Portal'

    # Plain text version
    text_content = (
        f'Hello {first_name} {last_name},\n\n'
        f'Your RDSO Portal account has been created successfully.\n\n'
        f'Login Information:\n\n'
        f'Email: {email}\n'
        f'Temporary Password: {password}\n\n'
        f'Login URL: {LOGIN_URL}\n\n'
        f'For security reasons please change your password after signing in.\n\n'
        f'If you did not request this account, please contact support immediately.\n\n'
        f'Regards,\n'
        f'RDSO Portal Team'
    )

    # HTML version rendered from template
    html_content = render_to_string('email/welcome.html', {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'login_url': LOGIN_URL,
    })

    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send(fail_silently=False)

        logger.info(f"[EMAIL_SENT] Welcome email delivered to {email}")
        return True

    except Exception as e:
        logger.error(f"[EMAIL_FAILED] Could not send email to {email}: {type(e).__name__}: {e}")
        return False
