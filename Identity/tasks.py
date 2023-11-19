# tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_change_password_email(user_email, token):
    subject = 'Change Password Token'
    message = f'Your one-time token for changing the password is: {token}'
    from_email = 'alisfryly075@gmail.com'  # Update with your email
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
