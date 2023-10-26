from typing import Optional, Tuple
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import Token
from .models import HotelOwner,HotelsAccount
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class AuthenticateHotel(JWTAuthentication):
    def authenticate(self, request: Request):
        user,token = super().authenticate(request)
        print(user)
        # if user:
            # print('hiiiiiiiiiiiiii')
            # hotel = HotelsAccount.objects.filter(owner=HotelOwner.objects.filter(user=request.user),is_active=True,is_logined=True,is_approved=True).exists()
            # if hotel:
            #     return hotel
            # else:
            #     raise AuthenticationFailed
