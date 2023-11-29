# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from QueraPyRate import settings
import logging

logger = logging.getLogger(__name__)


@shared_task()
def send_change_password_email(user_email, token):
    try:
        logger.info(f"Sending email to {user_email}")
        logger.info(f"Token: {token}")
        mail_subject = "Change Password Token"
        message = token
        to_email = user_email
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
        return "Done"
    except Exception as e:
        # Log any exceptions for debugging
        logger.exception(f"Error in send_change_password_email task{e}")
        raise
