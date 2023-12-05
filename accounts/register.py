from rest_framework.exceptions import AuthenticationFailed

# import random
from .models import MyUser
from . import views

# from django.contrib.auth import authenticate


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = MyUser.objects.filter(email=email)

    if filtered_user_by_email.exists():
        if provider == filtered_user_by_email[0].auth_provider:
            user = MyUser.objects.get(email=email)
            return {
                "username": user.username,
                "email": user.email,
                "tokens": views.get_tokens_for_user(user),
            }
        else:
            # in here they must enter their otp
            raise AuthenticationFailed(detail="Please Continue using otp.")
    else:
        user = {
            "email": email,
            "username": name,
        }
        user = MyUser.objects.create_user(**user)
        user.is_active = True
        user.save()
        return {
            "email": user.email,
            "username": user.username,
            "tokens": views.get_tokens_for_user(user),
        }
