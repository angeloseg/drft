from celery import shared_task
from django.core.mail import send_mail


@shared_task
def conf_email(email):
    send_mail(
        'Hey there Fella',
        'Welcome to the test Realm...\nHave Fun!!!',
        'aeggeorgiadis@gmail.com',
        [email],
        fail_silently=False,
    )
