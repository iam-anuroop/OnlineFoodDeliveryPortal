from celery import shared_task
from django.core.mail import send_mail,EmailMessage
from decouple import config
import asyncio



@shared_task
def send_mail_to_users(subject,message,recipient_list):
    sender = config('EMAIL_HOST_USER')
    for recipient_email in recipient_list:
        send_mail(subject,message,sender,[recipient_email])



# @shared_task
# def send_mail_to_users(subject, message, recipient_list):
#     sender = config('EMAIL_HOST_USER')

#     async def send_email(recipient_email):
#         email = EmailMessage(subject, message, sender, [recipient_email])
#         email.send()

#     loop = asyncio.get_event_loop()
#     tasks = [send_email(recipient_email) for recipient_email in recipient_list]
#     loop.run_until_complete(asyncio.gather(*tasks))

