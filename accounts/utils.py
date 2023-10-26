from twilio.rest import Client
from django.conf import settings
from twilio.base.exceptions import TwilioRestException
from django.core.mail import EmailMessage
from django.template.loader import render_to_string



client = Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
def send_phone(email):
    try: 
        print(email,'llll')
        verification = client.verify \
                        .v2 \
                        .services(settings.SERVICE_SID) \
                        .verifications \
                        .create(to=email, channel='sms')
        return verification.sid
    except ConnectionError as e:
        raise e
       

def verify_user_code(verification_sid, user_input):
# Initialize the Twilio client using your account SID and auth token

    # Verify the user-entered code against the verification SID
    try:
        verification_check = client.verify \
        .v2 \
        .services(settings.SERVICE_SID) \
        .verification_checks \
        .create(verification_sid=verification_sid, code=user_input)

    # Return the verification check status
        return verification_check.status
    except TwilioRestException as e:
        raise e
    


def send_email(user=None,email=None,message=None,otp=None,subject=None):
    mail_subject = subject
    message = render_to_string("email_otp.html", {
        'user': user,
        'otp':otp,
        'message':message
    })
    to_email = email
    send_mail = EmailMessage(mail_subject, message, to=[to_email])
    send_mail.send()











#     # Download the helper library from https://www.twilio.com/docs/python/install
# import os
# from twilio.rest import Client

# # Set environment variables for your credentials
# # Read more at http://twil.io/secure
# account_sid = "ACbdcbb885e863d4751c3e54d71cc2f0e1"
# auth_token = "4fafc14684661a9144a60af626f89e6d"
# verify_sid = "VAe297e90e4e232b83d4ddeeb303d6c96c"
# verified_number = "+917034256543"

# client = Client(account_sid, auth_token)

# verification = client.verify.v2.services(verify_sid) \
#   .verifications \
#   .create(to=verified_number, channel="sms")
# print(verification.status)

# otp_code = input("Please enter the OTP:")

# verification_check = client.verify.v2.services(verify_sid) \
#   .verification_checks \
#   .create(to=verified_number, code=otp_code)
# print(verification_check.status)