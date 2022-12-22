import random
from django.core.mail import send_mail
from django.conf import settings

from accounts.models import Account
from rest_framework.response import Response
from rest_framework import status


def send_otp_email(email):
    subject='your account verification email '
    otp=random.randint(1000,9999)
    message= f"your otp is {otp}"
    email_from=settings.EMAIL_HOST
    send_mail(subject,message,email_from,[email])
    return Response(status=status.HTTP_100_CONTINUE)
    user_obj=Account.objects.get(email=email)
    user_obj.email_otp=otp
    user_obj.save()

