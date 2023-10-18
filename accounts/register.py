from rest_framework.exceptions import AuthenticationFailed
import random
from .models import MyUser
from decouple import config
from . import views
from django.contrib.auth import authenticate


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = MyUser.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:
            register_user = authenticate(
                email=email, password= config('GOOGLE_CLIENT_SECRET')
            )
            print(register_user)
            
            return {
                'username':register_user.username,
                'email':register_user.email,
                'tokens':views.get_tokens_for_user(register_user)
            }
        else:
            raise AuthenticationFailed(
                detail="Please Continue your login using "+filtered_user_by_email[0].auth_provider
            )
    else:
        user = {
            'email':email,
            'password':config('GOOGLE_CLIENT_SECRET')
        }
        user = MyUser.objects.create_user(**user)
        user.auth_provider = 'google'
        user.is_active =True
        user.save()
        new_user = authenticate(
            email=email, password=config('GOOGLE_CLIENT_SECRET')
        )
        return{
            'email':new_user.email,
            'username':new_user.username,
            'tokens':views.get_tokens_for_user(new_user)
        }
