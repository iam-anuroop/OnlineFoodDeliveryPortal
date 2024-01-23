from twilio.rest import Client
from django.conf import settings
from twilio.base.exceptions import TwilioRestException
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)


def send_phone(phone):
    try:
        verification = client.verify.v2.services(
            settings.SERVICE_SID
        ).verifications.create(to=phone, channel="sms")
        return verification.sid
    except ConnectionError as e:
        raise e


def verify_user_code(verification_sid, user_input):
    # Initialize the Twilio client using your account SID and auth token

    # Verify the user-entered code against the verification SID
    try:
        verification_check = client.verify.v2.services(
            settings.SERVICE_SID
        ).verification_checks.create(verification_sid=verification_sid, code=user_input)

        # Return the verification check status
        return verification_check.status
    except TwilioRestException as e:
        raise e


def send_email(user=None, email=None, message=None, otp=None, subject=None):
    mail_subject = subject
    message = render_to_string(
        "email_otp.html", {"user": user, "otp": otp, "message": message}
    )
    to_email = email
    send_mail = EmailMessage(mail_subject, message, to=[to_email])
    send_mail.send()
    return "done"
