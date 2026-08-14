from celery import shared_task
from .models import *
from django.core.mail import send_mail

@shared_task(bind=True)
def send_otp(self, otp_id):
    otp_object = OTP.objects.get(id = otp_id)
    
    subject = 'Your otp code'
    message = f"Thankyou for register in our application. Your OTP code is {otp_object.otp}. It will expire in 5 minutes."
    
    send_mail(
        subject,
        message,
        None,
        [otp_object.email],
        fail_silently=False
    )
    return f"OTP sent to {otp_object.email}"